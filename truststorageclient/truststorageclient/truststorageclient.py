from truststorageclient.besuclient import add_besu, get_besu, deprecate_besu
from truststorageclient.restclient import add_ipfs, get_ipfs


def add_document(document:dict) -> str:
    cid = add_ipfs(document)
    add_besu(cid)
    return cid

def get_document(cid:str) -> dict:
    get_besu(cid)
    return get_ipfs(cid)

def deprecate_document(cid:str) -> None:
    deprecate_besu(cid)
