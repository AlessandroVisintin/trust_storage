from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from .models import NetworkConfig
from .crypto_service import CryptoService

class BaseGenerator(ABC):
    
    def __init__(self, crypto_service: CryptoService):
        self.crypto_service = crypto_service
    
    @abstractmethod
    def generate(self, config: NetworkConfig) -> None:
        pass
    
    def _extract_network_folder_binding(self, volumes: List[str]) -> Path:
        """Extract network folder path from volume bindings."""
        for volume in volumes:
            if ':/sources/network' in volume:
                return Path(volume.split(':')[0])
        raise ValueError("Network folder binding not found")
    
    def _extract_account_folder_binding(self, volumes: List[str]) -> Path:
        for volume in volumes:
            if ':/sources/account' in volume:
                return Path(volume.split(':')[0])
        raise ValueError("Account folder binding not found")
    
    def _get_p2p_endpoint(self, ports: List[str]) -> str:
        """Extract P2P endpoint from port bindings."""
        for port in ports:
            if port.endswith(':30303'):
                return port.split(':30303')[0]
        raise ValueError("P2P port binding not found")
