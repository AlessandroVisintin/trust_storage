import re
import rlp
from typing import List
from Crypto.Hash import keccak


def calculate_checksum_address(eth_address: str) -> str:
    address_lower = re.sub(r'0x', '', eth_address).lower()

    hash_obj = keccak.new(digest_bits=256)
    hash_obj.update(address_lower.encode('utf-8'))
    hash_hex = hash_obj.hexdigest()
    checksummed = ""
    for i, char in enumerate(address_lower):
        if char in 'abcdef':
            if int(hash_hex[i], 16) >= 8:
                checksummed += char.upper()
            else:
                checksummed += char
        else:
            checksummed += char
    return "0x" + checksummed

def calculate_contract_address(contract_name: str, prefix: str = "") -> str:
    address_string = f"{prefix}{contract_name}"
    address_hex = address_string.encode().hex()
    if len(address_hex) >= 40:
        return calculate_checksum_address(f"0x{address_hex[:40]}")
    return calculate_checksum_address(f"0x{address_hex.ljust(40, '0')}")

def calculate_qbft_extradata(validators: List[str]) -> str:
    vanity = b'\x00' * 32
    decoded = [bytes.fromhex(re.sub(r'0x', '', v)) for v in validators]
    vote = []
    round_number = 0
    seals = []
    payload = [vanity, decoded, vote, round_number, seals]
    return f"0x{rlp.encode(payload).hex()}"