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
    def load(filepath: str) -> EthAccount:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return EthAccount(
            private_key=data['private_key'],
            public_key=data['public_key'],
            eth_address=data['eth_address']
        )

    @staticmethod
    def dump(account: EthAccount, filepath: str) -> None:
        with open(filepath, 'w') as f:
            json.dump(asdict(account), f, indent=2)


class EthAccountRepository:

    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def generate(self, num:int=1) -> None:
      for _ in range(num):
        account = EthAccountGenerator.generate()
        filename = f'{account.eth_address.strip("0x")[:8].lower()}.json'
        EthAccountLoader.dump(account, os.path.join(self.folder_path, filename))

    def get(self, account_address: str) -> EthAccount:
        filepath = os.path.join(self.folder_path, account_address + '.json')
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Account with address {account_address} not found")
        return EthAccountLoader.load(filepath)

    def remove(self, account_address: str) -> EthAccount:
        filepath = os.path.join(self.folder_path, account_address + '.json')
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Account with address {account_address} not found")
        account = EthAccountLoader.load(filepath)
        os.remove(filepath)
        return account