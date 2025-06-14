import toml
from pathlib import Path
from typing import Dict, List

from .base_generator import BaseGenerator
from .config_models import NetworkConfig, ServiceConfig

class PermissionsGenerator(BaseGenerator):
    
    def generate(self, config: NetworkConfig) -> None:
        for service in config.services.values():
            nodes_allowlists = self._build_nodes_allowlist(service, config)
            accounts_allowlist = self._build_accounts_allowlist(service)
            allowlists = {}
            if nodes_allowlists:
                allowlists["nodes-allowlist"] = nodes_allowlists
            if accounts_allowlist:
                allowlists["accounts-allowlist"] = accounts_allowlist
            if allowlists:
                self._write_permissions_file(service, allowlists)

    def _build_nodes_allowlist(self, service: ServiceConfig, config: NetworkConfig) -> List:
        nodes_allowlist = []
        for node_name in service.node_config.nodes_allowlist:
            public_key = self.account_service.get_public_key_by_name(node_name)
            target_service = config.services.get(node_name)
            if target_service:
                p2p_endpoint = self._get_p2p_endpoint(target_service.ports)
                enode = f"enode://{public_key.strip('0x')}@{p2p_endpoint}"
                nodes_allowlist.append(enode)
        return nodes_allowlist
    
    def _build_accounts_allowlist(self, service: ServiceConfig) -> List:
        return [
            self.account_service.get_address_by_name(account_name)
            for account_name in service.node_config.accounts_allowlist
        ]
    
    def _write_permissions_file(self, service: ServiceConfig, allowlists: Dict) -> None:
        account_folder = self._extract_account_folder_binding(service.volumes)
        permissions_file = account_folder / "permissions_config.toml"
        
        permissions_file.parent.mkdir(parents=True, exist_ok=True)
        with open(permissions_file, 'w') as f:
            toml.dump(allowlists, f)
