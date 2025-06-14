from web3 import Web3

from .base_contract import BaseContract
from .adapter_models import BlockchainValue, BlockchainResponse, BlockchainError


class HashManager(BaseContract):

    def add(self, value: str, private_key: str) -> BlockchainResponse | BlockchainError:
        hashed_value = Web3.keccak(text=value)
        contract_function = self.contract.functions.add(hashed_value)
        return self.execute_transaction(contract_function, private_key)

    def read(self, hashed_value: str) -> BlockchainValue | BlockchainError:
        hashed_value = Web3.to_bytes(hexstr=hashed_value)
        contract_function = self.contract.functions.read(hashed_value)
        return self.call_function(contract_function)
    
    def deprecate(self, hashed_value: str, private_key: str) -> BlockchainResponse | BlockchainError:
        hashed_value = Web3.to_bytes(hexstr=hashed_value)
        contract_function = self.contract.functions.deprecate(hashed_value)
        return self.execute_transaction(contract_function, private_key)
