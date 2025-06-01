from dataclasses import dataclass

from .eth_account import EthAccount


@dataclass
class RPCEndpoint:
    endpoint: str


@dataclass
class P2PEndpoint:
    endpoint: str


@dataclass
class EthNode:
    account: EthAccount
    rpc_endpoint: RPCEndpoint
    p2p_endpoint: P2PEndpoint

    def enode(self):
        pubkey = self.account.public_key.strip("0x")
        return f"enode//{pubkey}@{self.p2p_endpoint}"