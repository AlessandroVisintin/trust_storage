from dataclasses import dataclass, field
from typing import List

from .accounts import Account


@dataclass
class EthEndpoints:
    rpc_endpoint: str
    p2p_endpoint: str


@dataclass
class EthNode:
    account: Account
    endpoints: EthEndpoints

    def get_rpc_url(self) -> str:
        return self.endpoints.rpc_endpoint
    
    def get_p2p_url(self) -> str:
        return self.endpoints.p2p_endpoint

    def get_enode(self):
        pubkey = self.account.public_key.strip("0x")
        return f"enode://{pubkey}@{self.p2p_endpoint}"


@dataclass
class EthNetwork:
    nodes: List[EthNode] = field(default_factory=list)
    
    def add_node(self, node: EthNode) -> None:
        if node not in self.nodes:
            self.nodes.append(node)
    
    def remove_node(self, node: EthNode) -> bool:
        try:
            self.nodes.remove(node)
            return True
        except ValueError:
            return False
    
    def get_node_count(self) -> int:
        return len(self.nodes)
    
    def by_address(self, address: str) -> List[EthNode]:
        return [node for node in self.nodes if node.account.address == address]
