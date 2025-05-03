from abc import ABC, abstractmethod
from typing import Dict, Any

from .blockchain import BlockchainInterface

class TransactionInterface(ABC):
    """Interface for handling blockchain transactions."""

    @abstractmethod
    def get_blockchain_client(self) -> BlockchainInterface :
        """ Returns underlying blockchain client"""
        pass

    @abstractmethod
    def create_transaction(self, to_address:str, data:Any, value:int, gas:str, gas_price:str) -> Dict[str, Any] :
        """ Creates a transaction."""
        pass

    @abstractmethod
    def send_signed_transaction(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        """Send a signed transaction."""
        pass

    @abstractmethod
    def get_transaction_receipt(self, txhash: str) -> Dict[str, Any]:
        """Get a transaction receipt."""
        pass
    
    @abstractmethod
    def process_receipt(self, receipt: Dict[str, Any]) -> Dict[str, Any]:
        """Process a transaction receipt and handle errors."""
        pass
