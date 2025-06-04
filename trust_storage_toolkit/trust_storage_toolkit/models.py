from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class ConsensusConfig:
    name: str
    parameters: Dict[str, Any]

@dataclass
class ContractConfig:
    path: str
    members: List[str]

@dataclass
class NodeConfig:
    is_bootnode: bool = False
    is_validator: bool = False
    accounts_allowlist: List[str] = field(default_factory=list)
    nodes_allowlist: List[str] = field(default_factory=list)

@dataclass
class ServiceConfig:
    name: str
    image: str
    volumes: List[str]
    ports: List[str]
    node_config: NodeConfig

@dataclass
class NetworkConfig:
    consensus: ConsensusConfig
    contracts: Optional[ContractConfig]
    services: Dict[str, ServiceConfig]

@dataclass
class Contract:
    name: str
    abi: List[Dict]
    bin: str
    bin_runtime: str
