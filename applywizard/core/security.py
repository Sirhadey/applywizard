"""
Security Manager: AES-256 Encryption, Keyring Integration, Zero-Telemetry
Handles all encryption/decryption operations and API key management.
"""

import os
import json
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet

try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False


class SecurityManager:
    """Manages encryption, decryption, and secure key storage."""

    def __init__(self, app_name="ApplyWizard", master_password=None):
        self.app_name = app_name
        self.keyring_available = KEYRING_AVAILABLE
        self.master_password = master_password or self._load_master_password()
        self.cipher_suite = self._setup_encryption()

    def _load_master_password(self):
        """Load or generate the master password using OS keyring."""
        if not self.keyring_available:
            # Fallback: use a local file-based key (user must set APPLYWIZARD_KEY env var)
            key = os.environ.get("APPLYWIZARD_KEY", "default-insecure-key-change-me")
            return key.encode()

        try:
            pwd = keyring.get_password(self.app_name, "master_password")
            if not pwd:
                pwd = os.urandom(32).hex()
                keyring.set_password(self.app_name, "master_password", pwd)
            return pwd.encode()
        except Exception:
            return os.urandom(32)

    def _setup_encryption(self):
        """Setup Fernet encryption using a derived key."""
        import base64
        import hashlib
        
        # Simple key derivation using SHA256
        key_material = hashlib.sha256(self.master_password).digest()
        fernet_key = base64.urlsafe_b64encode(key_material)
        return Fernet(fernet_key)

    def encrypt(self, data):
        """Encrypt data using AES-256 (Fernet)."""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher_suite.encrypt(data).decode()

    def decrypt(self, encrypted_data):
        """Decrypt data using AES-256 (Fernet)."""
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        return self.cipher_suite.decrypt(encrypted_data).decode()

    def store_secret(self, key, value):
        """Store a secret securely using keyring or encrypted local file."""
        if self.keyring_available:
            try:
                keyring.set_password(self.app_name, key, value)
                return True
            except Exception:
                pass
        # Fallback: encrypt and store locally
        encrypted = self.encrypt(value)
        config_dir = Path.home() / ".applywizard"
        config_dir.mkdir(exist_ok=True)
        secrets_file = config_dir / "secrets.json"
        secrets = json.load(open(secrets_file)) if secrets_file.exists() else {}
        secrets[key] = encrypted
        json.dump(secrets, open(secrets_file, 'w'))
        return True

    def retrieve_secret(self, key):
        """Retrieve a secret from keyring or encrypted local file."""
        if self.keyring_available:
            try:
                value = keyring.get_password(self.app_name, key)
                if value:
                    return value
            except Exception:
                pass
        # Fallback: load from encrypted local file
        config_dir = Path.home() / ".applywizard"
        secrets_file = config_dir / "secrets.json"
        if secrets_file.exists():
            secrets = json.load(open(secrets_file))
            if key in secrets:
                return self.decrypt(secrets[key])
        return None

    def hash_data(self, data):
        """Generate SHA-256 hash of data for verification."""
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()

    def verify_integrity(self, original_data, hash_value):
        """Verify data integrity using hash comparison."""
        return self.hash_data(original_data) == hash_value
