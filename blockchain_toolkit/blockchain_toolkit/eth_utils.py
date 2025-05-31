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

def snake_case_to_camel_case(value: str) -> str:
    data_list: list[str] = value.split("_")
    for i in range(1, len(data_list)):
        data_list[i] = data_list[i][0].upper() + data_list[i][1:]
    return "".join(data_list)
