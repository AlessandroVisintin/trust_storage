from abc import ABC, abstractmethod
from typing import Any

class ConfigurationInterface(ABC):
    """Interface for all configuration components"""
    @abstractmethod
    def get_endpoint(self) -> str:
        """Get the blockchain endpoint URL"""
        pass

    def get_contract_address(self) -> str:
        """Get the contract address"""
        pass
    
    @abstractmethod
    def get_contract_abi(self) -> str:
        """Get the contract ABI"""
        pass

    @abstractmethod
    def get_private_key(self) -> str:
        """Get the private key for transaction signing"""
        pass
    
    @abstractmethod
    def get_public_key(self) -> str:
        """Get the private key for transaction signing"""
        pass
