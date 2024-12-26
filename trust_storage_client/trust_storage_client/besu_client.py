from eth_abi import decode
from eth_account import Account
from web3 import Web3
import json
import os
import requests
import time

from trust_storage_client.utils import pem_to_hex


try:
    BESU_ENDPOINT = os.environ["BESU_ENDPOINT"]
    CONTRACT_ADDR_PATH = os.environ["CONTRACT_ADDR_PATH"]
    CONTRACT_JSON_PATH = os.environ["CONTRACT_JSON_PATH"]
    CLIENT_PRVKEY_PATH = os.environ["CLIENT_PRVKEY_PATH"]
    CLIENT_PUBKEY_PATH = os.environ["CLIENT_PUBKEY_PATH"]
except KeyError as e:
    raise ValueError(f"Missing ENV variable: {e}")


def read_contract_address():
    with open(CONTRACT_ADDR_PATH, 'r') as file:
        return file.read().strip()

def read_contract_abi() :
    with open(CONTRACT_JSON_PATH, 'r') as file:
        return file.read().strip()

def post(data:dict) -> dict:
    headers = {"Content-Type": "application/json"}
    response = requests.post(BESU_ENDPOINT, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return json.loads(response.content)

def wait_receipt(txhash:str, retry:int=60, interval:int=1) -> dict:
    while retry:
        d = {"jsonrpc": "2.0", "method": "eth_getTransactionReceipt", "params": [txhash], "id": 1}
        r = post(d)
        if r["result"] is not None:
            return r["result"]
        retry = retry - 1
        time.sleep(interval)        
    raise TimeoutError("Transaction receipt timed out")

def manage_receipt(txreceipt:dict) -> dict:
    status = txreceipt["status"]
    if status == "0x1":
        return txreceipt["logs"]
    
    txhash = txreceipt["transactionHash"]
    d = {"jsonrpc": "2.0", "method": "eth_getTransactionByHash", "params": [txhash], "id": 53}
    r = post(d)

    tx = r["result"]
    blockNum = tx["blockNumber"]
    d = {"jsonrpc": "2.0", "method": "eth_call", "params": [tx, blockNum], "id": 53}
    r = post(d)

    raise RuntimeError(r["error"]["message"])

def get_nonce(address:str) -> str:
    d = {"jsonrpc": "2.0", "method": "eth_getTransactionCount",
        "params": [address, "pending"], "id": 1}
    r = post(d)
    return r["result"]

def get_chainid() -> int:
    d = {"jsonrpc": "2.0", "method": "eth_chainId", "params": [], "id": 51}
    r = post(d)
    return r["result"]

def add_besu(document=str) -> None:
    account = Account.from_key(pem_to_hex(CLIENT_PRVKEY_PATH))
    contract_address = read_contract_address()
    contract_abi = read_contract_abi()
    contract = Web3().eth.contract(address=contract_address, abi=contract_abi)

    tx = {
        "from": account.address,
        "to": contract.address,
        "data": contract.encode_abi(abi_element_identifier="add", args=[Web3.keccak(text=document)]),
        "nonce": get_nonce(account.address),
        "chainId": get_chainid(),
        "gas": "0x1ffffffff",
        "gasPrice": "0x0",
    }

    raw = Web3.to_hex( account.sign_transaction(tx).raw_transaction )
    d = {"jsonrpc": "2.0", "method": "eth_sendRawTransaction", "params": [raw], "id": 1}
    r = post(d)

    return manage_receipt( wait_receipt( r["result"] ) )

def get_besu(cid:str) -> None:
    contract_address = read_contract_address()
    contract_abi = read_contract_abi()
    contract = Web3().eth.contract(address=contract_address, abi=contract_abi)
    data = contract.encode_abi(abi_element_identifier="read", args=[Web3.keccak(text=cid)])
    tx = {"to": contract.address, "data": data }

    d = {"jsonrpc": "2.0", "method": "eth_call", "params": [tx, "latest"], "id": 53}
    r = post(d)
    if "result" in r:
        return decode(['uint256', 'address'], bytes.fromhex(r["result"][2:])) 
    elif "error" in r:
        raise RuntimeError(r["error"]["message"])
    raise ValueError(f"Unexpected response format: {r}")

def deprecate_besu(cid=str) -> None:
    account = Account.from_key(pem_to_hex(CLIENT_PRVKEY_PATH))
    contract_address = read_contract_address()
    contract_abi = read_contract_abi()
    contract = Web3().eth.contract(address=contract_address, abi=contract_abi)

    tx = {
        "from": account.address,
        "to": contract.address,
        "data": contract.encode_abi(abi_element_identifier="deprecate", args=[Web3.keccak(text=cid)]),
        "nonce": get_nonce(account.address),
        "chainId": get_chainid(),
        "gas": "0x1ffffffff",
        "gasPrice": "0x0",
    }

    raw = Web3.to_hex( account.sign_transaction(tx).raw_transaction )
    d = {"jsonrpc": "2.0", "method": "eth_sendRawTransaction", "params": [raw], "id": 1}
    r = post(d)

    manage_receipt( wait_receipt( r["result"] ) )
