import json
from truststorageclient.truststorageclient import add_document, get_document, deprecate_document


###
#tbom = {"key":"value"}
with open("/src/tests/data/boms/xxl.json", 'r') as f:
    tbom = json.loads(f.read())

print(tbom.keys())

###
cid = add_document(tbom)
print(f"CID: {cid}")

###
print(f"Retrieving TBOM..")
retrieved = get_document(cid)
print(retrieved)

###
try:
    print(f"Try adding same TBOM..")
    cid = add_document(tbom)
    raise AssertionError("Expected RuntimeError")
except RuntimeError:
    print("RuntimeError correctly triggered")

###
CLIENT_PRVKEY_PATH="/src/tests/data/keys/user2/prvkey.pem"
CLIENT_PUBKEY_PATH="/src/tests/data/keys/user2/pubkey.pem"

###
try:
    print(f"Deprecating TBOM..")
    deprecate_document(cid)
    raise AssertionError("Expected RuntimeError")
except RuntimeError:
    print("RuntimeError correctly triggered")

###
CLIENT_PRVKEY_PATH="/src/tests/data/keys/user1/prvkey.pem"
CLIENT_PUBKEY_PATH="/src/tests/data/keys/user1/pubkey.pem"

###
print(f"Deprecating TBOM..")
deprecate_document(cid)

###
print(f"Trying reading deprecated TBOM..")
try:
    retrieved = get_document(cid)
    raise RuntimeError("Expected RuntimeError")
except RuntimeError:
    print("RuntimeError correctly triggered")
