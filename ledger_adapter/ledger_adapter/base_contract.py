import ast
from abc import ABC
from typing import Dict

from web3 import Web3
from web3.exceptions import Web3RPCError
from web3.middleware import ExtraDataToPOAMiddleware


class BaseContract(ABC):

    def __init__(
            self,
            contract_address: str,
            abi: Dict,
            node_url: str = "http://127.0.0.1:8545"
            ):
        self.w3 = Web3(Web3.HTTPProvider(node_url))
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        self.contract = self.w3.eth.contract(
            address=contract_address,
            abi=abi
        )

    def get_event_logs(self, event_name: str, from_block=0) -> list:
        event = getattr(self.contract.events, event_name)
        return event.get_logs(from_block=from_block)