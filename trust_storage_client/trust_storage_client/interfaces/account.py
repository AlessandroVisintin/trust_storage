from typing import Any
from abc import ABC, abstractmethod

class AccountInterface(ABC):
    
    @abstractmethod
    def get_address(self) -> str:
        """Get the Ethereum address."""
        pass

    def sign_transaction(self, tx:Any) -> Any :
        """Sign transaction."""
        pass
