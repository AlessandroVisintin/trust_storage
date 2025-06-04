from dataclasses import dataclass, field
from typing import List

from .accounts import Account
from .eth_network import EthEndpoints
from .besu_network import BesuNode


@dataclass
class QbftNode:
    besu_node: BesuNode
    is_validator: bool = False
    
    # Delegate operations through composition chain
    @property
    def account(self) -> Account:
        return self.besu_node.eth_node.account
    
    @property
    def endpoints(self) -> EthEndpoints:
        return self.besu_node.eth_node.endpoints
    
    @property
    def is_bootnode(self) -> bool:
        return self.besu_node.is_bootnode
    
    def can_validate_blocks(self) -> bool:
        return self.is_validator


@dataclass
class QbftNetwork:
    nodes: List[QbftNode] = field(default_factory=list)
    
    def add_node(self, node: QbftNode) -> None:
        if node not in self.nodes:
            self.nodes.append(node)
    
    def remove_node(self, node: QbftNode) -> bool:
        try:
            self.nodes.remove(node)
            return True
        except ValueError:
            return False
    
    def get_node_count(self) -> int:
        return len(self.nodes)
    
    def get_validators(self) -> List[QbftNode]:
        return [node for node in self.nodes if node.is_validator]
    
    def get_bootnodes(self) -> List[QbftNode]:
        return [node for node in self.nodes if node.besu_node.is_bootnode]
