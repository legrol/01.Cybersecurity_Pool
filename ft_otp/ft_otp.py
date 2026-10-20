#!/usr/bin/env python3

import argparse
import hashlib
import struct
import hmac
import time
import re
import os

from encryption_engine import EncryptionEngine


def parse_command_line_arguments():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(
        description="One-Time Password generator (HOTP core, TOTP mode)",
        epilog="Security Bootcamp - Málaga ft_otp assignment"
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)

    mode_group.add_argument(
        "-g",
        metavar="FILE",
        help="Store a hexadecimal key (minimum 64 characters) in encrypted 'ft_otp.key' file",
        type=str
    )
    mode_group.add_argument(
        "-k",
        metavar="FILE",
        help="Generate temporary password from encrypted key file",
        type=str
    )

    args = parser.parse_args()
    return args.g, args.k


def validate_key_file(filepath):
    """Validate that a file contains a valid hexadecimal key."""
    if not (os.path.isfile(filepath) and os.access(filepath, os.R_OK)):
        print(f"ft_otp: error: file '{filepath}' does not exist or is not readable.")
        return False, None

    with open(filepath, "r") as f:
        key_data = f.read().strip()

    if not re.match(r'^[0-9a-fA-F]{64,}$', key_data):
        print("ft_otp: error: key must be 64 hexadecimal characters.")
        return False, None

    return True, key_data


def is_valid_hex_key(key_data):
    """Return True only if key has valid hexadecimal format and minimum length."""
    return bool(re.match(r'^[0-9a-fA-F]{64,}$', key_data))


def generate_hotp_from_counter(secret_key, counter):
    """Generate a 6-digit HOTP code from a hex key and moving counter (RFC 4226)."""
    key_bytes = bytes.fromhex(secret_key)
    counter_bytes = struct.pack(">Q", counter)

    hash_result = hmac.digest(key_bytes, counter_bytes, hashlib.sha1)
    offset = hash_result[19] & 0x0f
    truncated = struct.unpack('>I', hash_result[offset:offset + 4])[0]
    otp_code = (truncated & 0x7fffffff) % 1000000

    return f"{otp_code:06d}"


def generate_totp_password(secret_key):
    """Generate TOTP using HOTP with time-window counter (RFC 6238 over RFC 4226)."""
    time_counter = int(time.time() // 30)
    return generate_hotp_from_counter(secret_key, time_counter)


def main():
    """Main program entry point."""
    key_input, pwd_generation = parse_command_line_arguments()

    # Handle key generation (-g flag)
    if key_input:
        is_valid, key_content = validate_key_file(key_input)
        if is_valid:
            # Save key to ft_otp.key file
            with open("ft_otp.key", "w") as f:
                f.write(key_content)

            print("Key was successfully saved in ft_otp.key.")

            # Encrypt the file
            engine = EncryptionEngine()
            engine.encrypt_file("ft_otp.key")
            print("File has been encrypted with password.")
        else:
            exit(1)

    # Handle password generation (-k flag)
    elif pwd_generation:
        if not (os.path.isfile(pwd_generation) and os.access(pwd_generation, os.R_OK)):
            print(f"ft_otp: error: file '{pwd_generation}' does not exist or is not readable.")
            exit(1)

        try:
            engine = EncryptionEngine()
            decrypted_key = engine.read_encrypted_file(pwd_generation)

            if not is_valid_hex_key(decrypted_key):
                print("ft_otp: error: decrypted key has invalid format.")
                exit(1)

            password = generate_totp_password(decrypted_key)
            print(password)

        except Exception as e:
            print(f"ft_otp: error: {str(e)}")
            exit(1)

if __name__ == "__main__":
    main()
