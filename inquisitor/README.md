# inquisitor

ARP poisoning tool (full duplex) + FTP filename sniffing for Linux.

## Mandatory requirements covered

- Takes at least 4 params: `<IP-src> <MAC-src> <IP-target> <MAC-target>`
- Works only with IPv4 (strict validation)
- Performs ARP poisoning in both directions
- Restores ARP tables on `CTRL+C` / stop
- Handles input and runtime exceptions without uncontrolled exits
- Sniffs FTP control traffic on port `21`
- Prints uploaded/downloaded file names in real time (`STOR` / `RETR`)

## Run

From project root:

```bash
python3 inquisitor.py <IP-src> <MAC-src> <IP-target> <MAC-target> -i <iface> [-v]
```

Example:

```bash
python3 inquisitor.py 172.22.0.1 aa:bb:cc:dd:ee:01 172.22.0.10 aa:bb:cc:dd:ee:10 -i eth0 -v
```

## Docker environment

The project includes `docker-compose` and a `Makefile` for non-interactive startup:

```bash
make up
make ps
make logs
make down
```

## FTP test checklist (evaluation-oriented)

1. Start lab environment (`make up`).
2. Verify traffic redirection (MITM node forwards packets).
3. Start `inquisitor.py` with gateway/victim IP+MAC.
4. From FTP client, upload a file (`STOR test.txt`).
5. Confirm real-time output shows `[FTP][UPLOAD] test.txt`.
6. Download a file (`RETR test.txt`).
7. Confirm output shows `[FTP][DOWNLOAD] test.txt`.
8. Stop with `CTRL+C` and verify ARP tables are restored.

## Notes

- Root privileges / `NET_ADMIN` + `NET_RAW` are required.
- Encrypted traffic is out of scope (as stated by evaluation rubric).

## Extra documentation

- Technical explanation: `Attachment/doc_tecnica.md`
- Evaluation runbook: `Attachment/guia_eval.md`
