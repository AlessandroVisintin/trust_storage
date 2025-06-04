# services/config_parser.py
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

from .models import NetworkConfig, ServiceConfig, NodeConfig, ConsensusConfig, ContractConfig

class ConfigParser:
    
    def parse(self, config_path: Path) -> NetworkConfig:
        with open(config_path, 'r') as file:
            data = yaml.safe_load(file)
        
        return NetworkConfig(
            consensus=self._parse_consensus(data.get('x-network-config', {}).get('consensus', {})),
            contracts=self._parse_contracts(data.get('x-network-config', {}).get('contracts')),
            services=self._parse_services(data.get('services', {}))
        )
    
    def _parse_consensus(self, consensus_data: Dict[str, Any]) -> ConsensusConfig:
        return ConsensusConfig(
            name=consensus_data.get('name', 'qbft'),
            parameters=consensus_data.get('parameters', {})
        )
    
    def _parse_contracts(self, contracts_data: Dict[str, Any]) -> Optional[ContractConfig]:
        if not contracts_data:
            return None
        return ContractConfig(
            path=contracts_data.get('path', ''),
            members=contracts_data.get('members', [])
        )
    
    def _parse_services(self, services_data: Dict[str, Any]) -> Dict[str, ServiceConfig]:
        services = {}
        for name, service_data in services_data.items():
            node_config_data = service_data.get('x-node-config', {})
            services[name] = ServiceConfig(
                name=name,
                image=service_data.get('image', ''),
                volumes=service_data.get('volumes', []),
                ports=service_data.get('ports', []),
                node_config=NodeConfig(
                    is_bootnode=node_config_data.get('is_bootnode', False),
                    is_validator=node_config_data.get('is_validator', False),
                    accounts_allowlist=node_config_data.get('accounts-allowlist', []),
                    nodes_allowlist=node_config_data.get('nodes-allowlist', [])
                )
            )
        return services
