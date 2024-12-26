import requests
import os

from truststorageclient.restclient import add_ipfs, get_ipfs


try:
    REST_ENDPOINT = os.environ["REST_ENDPOINT"]
except KeyError as e:
    raise ValueError(f"Missing ENV variable: {e}")

print(f"Check connectivity with {REST_ENDPOINT}..")
response = requests.get(REST_ENDPOINT)
response.raise_for_status()
print(response.content)

print(f"Add test TBOM..")
cid = add_ipfs({"test":"tbom"})
print(cid)

print(f"Get test TBOM..")
print(get_ipfs(cid))