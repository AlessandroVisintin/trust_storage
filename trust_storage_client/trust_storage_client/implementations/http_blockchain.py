import json
import requests
from typing import Dict, Any
from ..interfaces.blockchain import BlockchainInterface
from ..exceptions import BlockchainError

class HttpBlockchainClient(BlockchainInterface):
    """HTTP implementation of the blockchain interface."""
    
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.headers = {"Content-Type": "application/json"}
    
    def get_endpoint(self) -> str:
        return self.endpoint
    
    def post_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.post(
                self.endpoint, 
                headers=self.headers, 
                data=json.dumps(data)
            )
            response.raise_for_status()
            response = json.loads(response.content)
        except requests.exceptions.RequestException as e:
            raise BlockchainError(f"Failed to communicate with blockchain: {str(e)}")
        if 'result' in response:
            return response['result']
        if "error" in response:
            raise BlockchainError(response["error"]["message"])
        raise BlockchainError(f"Unexpected response format: {response}")

    def eth_call(self, tx:Dict[str, Any], block:str="latest") -> Dict[str, Any]:
        data = {"jsonrpc": "2.0", "method": "eth_call", 
                "params": [tx, block], "id": 53}
        return self.post_request(data)

    def get_nonce(self, address: str) -> str:
        data = {"jsonrpc": "2.0", "method": "eth_getTransactionCount",
                "params": [address, "pending"], "id": 1}
        return self.post_request(data)
    
    def get_chain_id(self) -> int:
        data = {"jsonrpc": "2.0", "method": "eth_chainId", "params": [], "id": 51}
        return self.post_request(data)
