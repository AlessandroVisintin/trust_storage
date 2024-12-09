from truststorageclient.besuclient import get_chainid, add_besu, get_besu, deprecate_besu


print(f"Check connectivity with BESU node..")
print( get_chainid() )

cid = "test cid"

print(f"Add test CID..")
add_besu(cid)

print(f"Add already exisitng hash..")
try:
    add_besu(cid)
    raise AssertionError("Expected RuntimeError")
except RuntimeError:
    print("RuntimeError correctly triggered")

print(f"Get CID..")
get_besu(cid)

print(f"Get not existing CID..")
try:
    get_besu("lol")
    raise AssertionError("Expected RuntimeError")
except RuntimeError:
    print("RuntimeError correctly triggered")

print(f"Deprecate CID..")
deprecate_besu(cid)

print(f"Deprecate already deprecated CID..")
try:
    deprecate_besu(cid)
    raise AssertionError("Expected RuntimeError")
except RuntimeError:
    print("RuntimeError correctly triggered")
