import ast
from abc import ABC
from typing import Dict

from eth_account import Account
from web3 import Web3
from web3.contract.contract import ContractFunction
from web3.exceptions import Web3RPCError
from web3.middleware import ExtraDataToPOAMiddleware

from .adapter_utils import parse_response_from_receipt, parse_error
from .adapter_models import BlockchainValue, BlockchainResponse, BlockchainError


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

    def execute_transaction(
        self,
        contract_function: ContractFunction,
        private_key: str
    ) -> BlockchainResponse | BlockchainError:

        try:
            account = Account.from_key(private_key)
            nonce = self.w3.eth.get_transaction_count(account.address)
            tx_params = {
                'from': account.address,
                'chainId': self.w3.eth.chain_id,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce
            }

            gas_estimate = contract_function.estimate_gas(tx_params)
            tx_params['gas'] = int(gas_estimate * 1.2)
            tx = contract_function.build_transaction(tx_params)
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return parse_response_from_receipt(self.contract, receipt)
        
        except Web3RPCError as e:
            return parse_error(e)

    def call_function(
            self,
            contract_function: ContractFunction
    ) -> BlockchainValue | BlockchainError:
    
        try:
            return BlockchainValue(value=contract_function.call())
        except Exception as e:
            return BlockchainError(message=str(e))
