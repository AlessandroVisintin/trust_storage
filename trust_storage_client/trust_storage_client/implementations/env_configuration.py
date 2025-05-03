import os
from typing import Any

from ..interfaces.configuration import ConfigurationInterface

class EnvConfiguration(ConfigurationInterface):
    """Implementation of ConfigurationInterface using environment variables"""
    
    def __init__(self):
        """Initialize and validate all configuration values"""

        self._endpoint = os.environ.get('BLOCKCHAIN_ENDPOINT')
        if not self._endpoint:
            raise ValueError("BLOCKCHAIN_ENDPOINT environment variable not set")
        
        self._contract_address = self._from_file('CONTRACT_ADDRESS_FILE')
        self._contract_abi = self._from_file('CONTRACT_ABI_FILE')
        self._private_key = self._from_file('PRIVATE_KEY_FILE')
        self._public_key = self._from_file('PUBLIC_KEY_FILE')
    
    def _from_file(self, env_var_name: str) -> str:
        """Helper method to read content from a file specified by an environment variable"""
        file_path = os.environ.get(env_var_name)
        if not file_path:
            raise ValueError(f"{env_var_name} environment variable not set")
        try:
            with open(file_path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path} (from {env_var_name})")
    
    def get_endpoint(self) -> str:
        """Get the blockchain endpoint URL"""
        return self._endpoint
    
    def get_contract_address(self) -> str:
        """Get the contract address"""
        return self._contract_address
    
    def get_contract_abi(self) -> str:
        """Get the contract ABI"""
        return self._contract_abi
    
    def get_private_key(self) -> str:
        """Get the private key for transaction signing"""
        return self._private_key
    
    def get_public_key(self) -> str:
        """Get the public key"""
        return self._public_key
