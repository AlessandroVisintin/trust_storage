from dataclasses import dataclass, field
from typing import List

from .accounts import Account
from .eth_network import EthEndpoints, EthNode


@dataclass
class BesuPermissions:
    account_permissions: List[str] = field(default_factory=list)
    node_permissions: List[str] = field(default_factory=list)


@dataclass
class BesuNode:
    eth_node: EthNode
    is_bootnode: bool = False
    permissions: BesuPermissions = field(default_factory=BesuPermissions)
    
    @property
    def account(self) -> Account:
        return self.eth_node.account
    
    @property
    def endpoints(self) -> EthEndpoints:
        return self.eth_node.endpoints
    
    def can_transact_with(self, account_address: str) -> bool:
        return account_address in self.permissions.account_permissions
    
    def can_communicate_with(self, node_id: str) -> bool:
        return node_id in self.permissions.node_permissions


@dataclass
class BesuNetwork:
    nodes: List[BesuNode] = field(default_factory=list)
    
    def add_node(self, node: BesuNode) -> None:
        if node not in self.nodes:
            self.nodes.append(node)
    
    def remove_node(self, node: BesuNode) -> bool:
        try:
            self.nodes.remove(node)
            return True
        except ValueError:
            return False
    
    def get_node_count(self) -> int:
        return len(self.nodes)
    
    def get_bootnodes(self) -> List[BesuNode]:
        return [node for node in self.nodes if node.is_bootnode]
