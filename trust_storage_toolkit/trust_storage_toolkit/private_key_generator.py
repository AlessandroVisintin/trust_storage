# generators/private_key_generator.py
from pathlib import Path

from .base_generator import BaseGenerator
from .models import NetworkConfig


class PrivateKeyGenerator(BaseGenerator):
    
    def generate(self, config: NetworkConfig) -> None:
        for service in config.services.values():
            self._generate_private_key_file(service)
    
    def _generate_private_key_file(self, service) -> None:
        private_key = self.crypto_service.get_private_key_by_name(service.name)
        account_folder = self._extract_account_folder_binding(service.volumes)
        self._dump_private_key_as_txt(private_key, account_folder)
    
    def _dump_private_key_as_txt(self, private_key: str, account_folder: Path) -> None:
        account_folder.mkdir(parents=True, exist_ok=True)
        key_file = account_folder / "key"

        with open(key_file, 'w') as f:
            f.write(private_key.strip('0x'))  # Remove 0x prefix for raw hex
        
        key_priv_file = account_folder / "key.priv"
        with open(key_priv_file, 'w') as f:
            f.write(private_key)  # Keep 0x prefix for this one
        
        print(f"Generated private key file for {account_folder.name}")
