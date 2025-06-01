import secrets
import json
import os
from dataclasses import dataclass, asdict
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import keccak

from .eth_utils import to_checksum_address

@dataclass
class EthAccount:
    private_key: str
    public_key: str
    eth_address: str


class EthAccountGenerator:

    @staticmethod
    def generate() -> EthAccount:
        # Generate a new private key
        private_key_bytes = secrets.randbits(256).to_bytes(32, 'big')
        private_key_hex = '0x' + private_key_bytes.hex()
        
        # Derive the public key
        signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
        public_key_bytes = signing_key.get_verifying_key().to_string()
        public_key_hex = '0x' + public_key_bytes.hex()
        
        # Derive the Ethereum address
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(public_key_bytes)
        address_bytes = keccak_hash.digest()[-20:]
        eth_address = '0x' + address_bytes.hex()
        
        return EthAccount(
            private_key=private_key_hex,
            public_key=public_key_hex,
            eth_address=to_checksum_address(eth_address)
            )


class EthAccountLoader:

    @staticmethod
    def load(folderpath: str) -> EthAccount:

        def _read(name):
            with open(os.path.join(folderpath, name), 'r') as f:
                return f.read().strip()

        return EthAccount(
            private_key=_read('private.key'),
            public_key=_read('public.key'),
            eth_address=_read('eth.address')
        )

    @staticmethod
    def dump(account: EthAccount, folderpath: str) -> None:

        def _write(value, name):
            with open(os.path.join(folderpath, name), 'w') as f:
                f.write(value)
        
        _write(account.private_key, 'private.key')
        _write(account.public_key, 'public.key')
        _write(account.eth_address, 'eth.address')


class EthAccountRepository:

    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def generate(self, name: str) -> None:
        account_dir = os.path.join(self.folder_path, name)
        if os.path.exists(account_dir):
            raise FileExistsError(f"An account named '{name}' already exists.")
        os.makedirs(account_dir, exist_ok=False)
        account = EthAccountGenerator.generate()
        EthAccountLoader.dump(account, account_dir)
        return account

    def get(self, name: str) -> EthAccount:
        account_dir = os.path.join(self.folder_path, name)
        if not os.path.exists(account_dir):
            raise FileNotFoundError(f"Account named {name} not found")
        return EthAccountLoader.load(account_dir)
