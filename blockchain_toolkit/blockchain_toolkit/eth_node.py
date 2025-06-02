import json
from pathlib import Path
from typing import List, Optional
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
    bootnode: bool

    def enode(self):
        pubkey = self.account.public_key.strip("0x")
        return f"enode//{pubkey}@{self.p2p_endpoint}"
