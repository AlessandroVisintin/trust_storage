from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from .config_models import NetworkConfig
from .account_service import AccountService


class BaseGenerator(ABC):
    
    def __init__(self, account_service: AccountService, base_path: Path):
        self.account_service = account_service
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

    def _generate_enode(self, public_key: str, p2p_endpoint: str) -> str:
        return f"enode://{public_key[2:]}@{p2p_endpoint}"
