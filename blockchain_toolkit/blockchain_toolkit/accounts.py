import secrets
from dataclasses import dataclass
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import keccak
from pathlib import Path
import json

from .utils import to_checksum_address

@dataclass
class Account:
    name: str
    private_key: str
    public_key: str
    address: str


class AccountGenerator:

    @staticmethod
    def generate_private_key() -> str:
        private_key_bytes = secrets.randbits(256).to_bytes(32, 'big')
        return '0x' + private_key_bytes.hex()

    @staticmethod
    def derive_public_key(private_key: str) -> str:
        private_key_bytes = bytes.fromhex(private_key[2:])
        signing_key = SigningKey.from_string(
            private_key_bytes,
            curve=SECP256k1
            )
        public_key_bytes = signing_key.get_verifying_key().to_string()
        return '0x' + public_key_bytes.hex()

    @staticmethod
    def derive_address(public_key: str) -> str:
        public_key_bytes = bytes.fromhex(public_key[2:])
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(public_key_bytes)
        address_bytes = keccak_hash.digest()[-20:]
        return to_checksum_address('0x' + address_bytes.hex())


class AccountRepository:

    def __init__(self, folder_path: str):
        self.folder_path = Path(folder_path)
        self.folder_path.mkdir(parents=True, exist_ok=True)

    def save(self, account: Account) -> None:
        file_path = self.folder_path / f"{account.name}.json"
        file_path.write_text(json.dumps(account.__dict__))
    
    def load(self, name: str) -> Account:
        file_path = self.folder_path / f"{name}.json"
        if not file_path.exists():
            return None
        data = json.loads(file_path.read_text())
        return Account(**data)

    def delete(self, name: str) -> Account:
        file_path = self.folder_path / f"{name}.json"
        if not file_path.exists():
            return None
        account = self.load(name)
        file_path.unlink()
        return account
