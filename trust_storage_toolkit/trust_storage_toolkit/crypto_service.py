# services/crypto_service.py
import secrets
from typing import Dict, List
from Crypto.Hash import keccak
from ecdsa import SigningKey, SECP256k1
from eth_utils import to_checksum_address
import rlp


class CryptoService:
    
    def __init__(self):
        self._private_keys: Dict[str, str] = {}
        self._public_keys: Dict[str, str] = {}
        self._addresses: Dict[str, str] = {}
    
    def generate_private_key(self) -> str:
        private_key_bytes = secrets.randbits(256).to_bytes(32, 'big')
        return '0x' + private_key_bytes.hex()
    
    def derive_public_key(self, private_key: str) -> str:
        private_key_bytes = bytes.fromhex(private_key[2:])
        signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
        public_key_bytes = signing_key.get_verifying_key().to_string()
        return '0x' + public_key_bytes.hex()
    
    def derive_address(self, public_key: str) -> str:
        public_key_bytes = bytes.fromhex(public_key[2:])
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(public_key_bytes)
        address_bytes = keccak_hash.digest()[-20:]
        return to_checksum_address('0x' + address_bytes.hex())
    
    def get_private_key_by_name(self, name: str) -> str:
        if name not in self._private_keys:
            self._private_keys[name] = self.generate_private_key()
        return self._private_keys[name]
    
    def get_public_key_by_name(self, name: str) -> str:
        if name not in self._public_keys:
            private_key = self.get_private_key_by_name(name)
            self._public_keys[name] = self.derive_public_key(private_key)
        return self._public_keys[name]
    
    def get_address_by_name(self, name: str) -> str:
        if name not in self._addresses:
            public_key = self.get_public_key_by_name(name)
            self._addresses[name] = self.derive_address(public_key)
        return self._addresses[name]
    
    def calculate_qbft_extradata(self, validators: List[str]) -> str:
        """Calculate QBFT extradata for genesis block."""
        vanity = b'\x00' * 32
        decoded = [bytes.fromhex(v.strip("0x")) for v in validators]
        vote = []
        round_number = 0
        seals = []
        payload = [vanity, decoded, vote, round_number, seals]
        return f"0x{rlp.encode(payload).hex()}"
