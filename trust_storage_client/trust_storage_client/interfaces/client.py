from abc import ABC, abstractmethod
from typing import Any, Dict

class ClientInterface(ABC):
    """Abstract base class for blockchain clients"""

    @abstractmethod
    def execute_transaction(self, function_name: str, args: list) -> Dict[str, Any]:
        """Execute a contract transaction"""
        pass

    @abstractmethod
    def call_contract_function(self, function_name: str, args: list) -> Any:
        """Call a contract view function"""
        pass
