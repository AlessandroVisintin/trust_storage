from abc import ABC, abstractmethod
from typing import Dict, Any

class BlockchainInterface(ABC):
    """Interface for interacting with a blockchain node."""
    
    @abstractmethod
    def post_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a request to the blockchain node."""
        pass
    
    @abstractmethod
    def eth_call(self, tx: Dict[str, Any], block:str) -> Dict[str, Any]:
        """Perform an eth_call to the blockchain node."""
        pass
    
    @abstractmethod
    def get_nonce(self, address: str) -> str:
        """Get the next nonce for an address."""
        pass
    
    @abstractmethod
    def get_chain_id(self) -> int:
        """Get the chain ID."""
        pass
