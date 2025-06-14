from .base_contract import BaseContract
from .adapter_models import BlockchainValue, BlockchainResponse, BlockchainError


class SimpleStorage(BaseContract):

    def set(self, new_value: str, private_key: str) -> BlockchainResponse | BlockchainError:
        contract_function = self.contract.functions.set(new_value)
        return self.execute_transaction(contract_function, private_key)

    def get(self) -> BlockchainValue | BlockchainError:
        contract_function = self.contract.functions.get()
        return self.call_function(contract_function)
