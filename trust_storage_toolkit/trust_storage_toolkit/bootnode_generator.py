from typing import List

from .base_generator import BaseGenerator
from .models import NetworkConfig

class BootnodeGenerator(BaseGenerator):
    
    def generate(self, config: NetworkConfig) -> None:
        bootnodes = self._collect_bootnodes(config)
        self._write_bootnode_files(bootnodes)
    
    def _collect_bootnodes(self, config: NetworkConfig) -> List[str]:
        bootnodes = []
        
        for service in config.services.values():
            if not service.node_config.is_bootnode:
                continue
            
            public_key = self.crypto_service.get_public_key_by_name(service.name)
            p2p_endpoint = self._get_p2p_endpoint(service.ports)
            
            enode = f"enode://{public_key.strip('0x')}@{p2p_endpoint}"
            bootnodes.append(enode)
        
        return bootnodes
    
    def _write_bootnode_files(self, bootnodes: List[str]) -> None:
        bootnode_file = self.base_path / "bootnodes.txt"
        bootnode_file.parent.mkdir(parents=True, exist_ok=True)
        with open(bootnode_file, 'w') as f:
            for bootnode in bootnodes:
                f.write(f"{bootnode}\n")
