import getpass
import hashlib
import hmac
import os
import sys


class EncryptionEngine:
    """Password-based authenticated encryption engine using only Python stdlib."""

    MAGIC = b"FTOTP1"
    SALT_SIZE = 16
    NONCE_SIZE = 16
    TAG_SIZE = 32
    PBKDF2_ROUNDS = 200000

    def __init__(self):
        pass

    def _get_password(self, prompt):
        """Get password from user, handling both interactive and piped input."""
        if sys.stdin.isatty():
            return getpass.getpass(prompt).encode("utf-8")
        else:
            return input(prompt).encode("utf-8")

    def _derive_keys(self, password, salt):
        """Derive independent encryption and authentication keys from password."""
        material = hashlib.pbkdf2_hmac(
            "sha256",
            password,
            salt,
            self.PBKDF2_ROUNDS,
            dklen=64,
        )
        return material[:32], material[32:]

    def _keystream_xor(self, data, enc_key, nonce):
        """Encrypt/decrypt bytes via HMAC-based keystream XOR."""
        output = bytearray()
        counter = 0

        while len(output) < len(data):
            block = hmac.new(
                enc_key,
                nonce + counter.to_bytes(8, "big"),
                hashlib.sha256,
            ).digest()
            output.extend(block)
            counter += 1

        return bytes(a ^ b for a, b in zip(data, output[: len(data)]))

    def encrypt_data(self, plaintext_data):
        """Encrypt plaintext and return an authenticated binary payload."""
        password = self._get_password("Enter password: ")

        if len(password) != 16:
            print("Password must be exactly 16 characters.")
            exit(1)

        salt = os.urandom(self.SALT_SIZE)
        nonce = os.urandom(self.NONCE_SIZE)
        enc_key, mac_key = self._derive_keys(password, salt)

        plaintext = plaintext_data.encode("utf-8")
        ciphertext = self._keystream_xor(plaintext, enc_key, nonce)

        payload = self.MAGIC + salt + nonce + ciphertext
        tag = hmac.new(mac_key, payload, hashlib.sha256).digest()
        return payload + tag

    def decrypt_data(self, encrypted_data):
        """Decrypt and verify authenticated payload."""
        password = self._get_password("Enter password: ")

        if len(password) != 16:
            print("Password must be exactly 16 characters.")
            exit(1)

        try:
            min_size = len(self.MAGIC) + self.SALT_SIZE + self.NONCE_SIZE + self.TAG_SIZE
            if len(encrypted_data) < min_size or not encrypted_data.startswith(self.MAGIC):
                raise ValueError("Invalid file format.")

            salt_start = len(self.MAGIC)
            salt_end = salt_start + self.SALT_SIZE
            nonce_end = salt_end + self.NONCE_SIZE

            salt = encrypted_data[salt_start:salt_end]
            nonce = encrypted_data[salt_end:nonce_end]
            ciphertext = encrypted_data[nonce_end:-self.TAG_SIZE]
            recv_tag = encrypted_data[-self.TAG_SIZE:]

            enc_key, mac_key = self._derive_keys(password, salt)
            payload = encrypted_data[:-self.TAG_SIZE]
            calc_tag = hmac.new(mac_key, payload, hashlib.sha256).digest()

            if not hmac.compare_digest(recv_tag, calc_tag):
                raise ValueError("Authentication failed.")

            plaintext = self._keystream_xor(ciphertext, enc_key, nonce)
            return plaintext.decode("utf-8")
        except Exception:
            print("Incorrect password.")
            exit(1)

    def encrypt_file(self, filepath):
        """Encrypt file contents and overwrite the file with bytes."""
        with open(filepath, "r") as f:
            content = f.read()

        encrypted_content = self.encrypt_data(content)

        with open(filepath, "wb") as f:
            f.write(encrypted_content)

        return encrypted_content

    def decrypt_file(self, filepath):
        """Decrypt file contents and overwrite the file."""
        with open(filepath, "rb") as f:
            content = f.read()

        decrypted_content = self.decrypt_data(content)

        with open(filepath, "w") as f:
            f.write(decrypted_content)

        return decrypted_content

    def read_encrypted_file(self, filepath):
        """Read and decrypt file contents without modifying the file."""
        with open(filepath, "rb") as f:
            content = f.read()

        return self.decrypt_data(content)
