from typing import Any
from datetime import datetime, timezone, timedelta
import jwt
import os
import requests
import json


try:
    REST_ENDPOINT = os.environ["REST_ENDPOINT"]
    CLIENT_PRVKEY_PATH = os.environ["CLIENT_PRVKEY_PATH"]
    CLIENT_PUBKEY_PATH = os.environ["CLIENT_PUBKEY_PATH"]
except KeyError as e:
    raise ValueError(f"Missing ENV variable: {e}")


def read_prvkey(mode:str='r') -> str:
    with open (CLIENT_PRVKEY_PATH, mode) as f:
        return f.read().strip()

def read_pubkey(mode:str='r') -> str:
    with open (CLIENT_PUBKEY_PATH, mode) as f:
        return f.read().strip()

def prepare_jwt(document:dict, expire_delta:int=60, algorithm:str="ES256") -> str:
    return jwt.encode(
        {
            "iss": "rescale",
            "sub": "TrustStorageClient",
            "iat": datetime.now(tz=timezone.utc),
            "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expire_delta),
            "tbom": document
        },
        key=read_prvkey(),
        algorithm=algorithm
    )

def add_ipfs(document:dict) -> str:
    headers = {"Content-Type": "application/json"}
    data = {"jwt": prepare_jwt(document), "public_key": read_pubkey()}
    response = requests.post(f"{REST_ENDPOINT}/create", headers=headers, data=json.dumps(data))
    response.raise_for_status()
    content = json.loads(response.content)
    try:
        return content["response"]["Hash"]
    except KeyError:
        print(f"Error: {content["error"]}")
        return None

def get_ipfs(cid:str) -> str:
    response = requests.get(f"{REST_ENDPOINT}/cat/{cid}")
    response.raise_for_status()
    content = json.loads(response.content)
    try:
        return content["tbom"]
    except KeyError:
        print(f"Error: {content["error"]}")
        return None
