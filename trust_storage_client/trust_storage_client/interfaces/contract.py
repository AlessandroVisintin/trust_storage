from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ContractInterface(ABC):
    """Interface for interacting with a smart contract."""
    
    @abstractmethod
    def get_address(self) -> str:
        """Get the contract address."""
        pass

    @abstractmethod
    def call(self, function_name: str, args: list) -> Any:
        """Call simple function with no transaction involved."""
        pass
    
    @abstractmethod
    def execute(self, function_name: str, args: list) -> Dict[str, Any]:
        """ Execute function that requires a transaction."""
        pass
 