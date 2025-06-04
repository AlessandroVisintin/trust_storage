from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from .models import NetworkConfig
from .crypto_service import CryptoService

class BaseGenerator(ABC):
    
    def __init__(self, crypto_service: CryptoService, base_path: Path):
        self.crypto_service = crypto_service
        self.base_path = base_path
    
    @abstractmethod
    def generate(self, config: NetworkConfig) -> None:
        pass
    
    def _extract_network_folder_binding(self, volumes: List[str]) -> Path:
        for volume in volumes:
            if ':/sources/network' in volume:
                return self.base_path / Path(volume.split(':')[0])
        raise ValueError("Network folder binding not found")
    
    def _extract_account_folder_binding(self, volumes: List[str]) -> Path:
        for volume in volumes:
            if ':/sources/account' in volume:
                return self.base_path / Path(volume.split(':')[0])
        raise ValueError("Account folder binding not found")
    
    def _get_p2p_endpoint(self, ports: List[str]) -> str:
        for port in ports:
            if port.endswith(':30303'):
                splitted = port.split(':')
                return ":".join(splitted[:-1])
        raise ValueError("P2P port binding not found")
