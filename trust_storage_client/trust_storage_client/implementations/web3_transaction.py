import time
from typing import Dict, Any
from web3 import Web3
from eth_account import Account

from ..interfaces.blockchain import BlockchainInterface
from ..interfaces.transaction import TransactionInterface
from ..exceptions import TransactionError, TransactionTimeoutError

class Web3Transaction(TransactionInterface):
    
    def __init__(self, blockchain_client:BlockchainInterface, private_key:str):
        self.blockchain_client = blockchain_client
        self.account = Account.from_key(private_key)
    
    def get_blockchain_client(self) -> BlockchainInterface :
        return self.blockchain_client

    def create_transaction(self, to_address:str, data:Any=None, value:int=None, gas:str="0x1ffffffff", gas_price:str="0x0") -> Dict[str, Any]:
        tx = {
            "from": self.account.address,
            "to": to_address,
            "gas": gas,
            "gasPrice": gas_price,
            "nonce": self.blockchain_client.get_nonce(self.account.address),
            "chainId": self.blockchain_client.get_chain_id()
        }
        if value is not None:
            tx["value"] = value
        if data is not None:
            tx["data"] = data
        return tx

    def send_signed_transaction(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        signed_tx = self.account.sign_transaction(tx)
        signed_raw_tx = Web3.to_hex(signed_tx.raw_transaction)
        data = {"jsonrpc": "2.0", "method": "eth_sendRawTransaction", 
                "params": [signed_raw_tx], "id": 1}
        return self.blockchain_client.post_request(data)

    def get_transaction_receipt(self, txhash: str, retry: int = 60, interval: int = 1) -> Dict[str, Any]:
        remaining_retries = retry
        while remaining_retries:
            data = {
                "jsonrpc": "2.0", 
                "method": "eth_getTransactionReceipt", 
                "params": [txhash], 
                "id": 1
            }
            response = self.blockchain_client.post_request(data)
            if response is not None:
                return response
            remaining_retries -= 1
            time.sleep(interval)        
        raise TransactionTimeoutError("Transaction receipt timed out")
    
    def process_receipt(self, receipt: Dict[str, Any]) -> Dict[str, Any]:
        status = receipt["status"]
        if status == "0x1":
            return receipt["logs"]
        txhash = receipt["transactionHash"]
        data = {"jsonrpc": "2.0", "method": "eth_getTransactionByHash", 
                "params": [txhash], "id": 53}
        tx = self.blockchain_client.post_request(data)
        block_num = tx["blockNumber"]
        response = self.blockchain_client.eth_call(tx, block_num)
        if "error" in response:
            raise TransactionError(response["error"]["message"])
        raise TransactionError("Transaction failed for unknown reason")
