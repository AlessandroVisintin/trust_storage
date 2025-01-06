from trust_storage_client.besu_client import get_chainid, add_besu, get_besu, deprecate_besu


print(f"Check connectivity with BESU node..")
print( get_chainid() )


with open("/sources/trust_storage_client/tests/data/boms/xxl.json") as f:
    bom = f.read()


print(f"Add test BOM..")
ahash = (add_besu(bom))['hash']

print(f"Add already exisitng hash..")
try:
    add_besu(bom)
    raise AssertionError("Expected RuntimeError")
except RuntimeError:
    print("RuntimeError correctly triggered")


print(f"Check BOM hash..")
get_besu(ahash)

print(f"Get not existing hash..")
try:
    get_besu("0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef")
    raise AssertionError("Expected RuntimeError")
except RuntimeError:
    print("RuntimeError correctly triggered")


print(f"Deprecate BOM hash..")
deprecate_besu(ahash)

print(f"Deprecate already deprecated CID..")
try:
    deprecate_besu(ahash)
    raise AssertionError("Expected RuntimeError")
except RuntimeError:
    print("RuntimeError correctly triggered")

print(f"Get deprecated hash..")
try:
    get_besu(ahash)
    raise AssertionError("Expected RuntimeError")
except RuntimeError:
    print("RuntimeError correctly triggered")

