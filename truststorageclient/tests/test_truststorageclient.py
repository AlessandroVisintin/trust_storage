import json
import sys
from truststorageclient.truststorageclient import add_document, get_document, deprecate_document


print("Loading BOM..")
tbom = {"test":"tbom"}
#with open('data/boms/xsmall.json', 'r') as f:
#    tbom = json.loads(f.read())

print(f"TBOM size: {sys.getsizeof(tbom)}")

print(f"Adding TBOM..")
cid = add_document(tbom)
print(f"CID: {cid}")

print(f"Retrieving TBOM..")
retrieved = get_document(cid)
print(f"TBOM size: {sys.getsizeof(retrieved)}")

print(f"Deprecating TBOM..")
deprecate_document(cid)

print(f"Trying reading deprecated TBOM..")
try:
    retrieved = get_document(cid)
    raise RuntimeError("Expected RuntimeError")
except RuntimeError:
    print("RuntimeError correctly triggered")
