# trust_storage

from Crypto.Hash import keccak


def to_checksum_address(eth_address) -> str:
    address_lower = eth_address.strip('0x').lower()
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