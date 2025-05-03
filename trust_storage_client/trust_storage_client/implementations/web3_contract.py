from web3 import Web3
from typing import Dict, Any, List

from ..exceptions import ContractError
from ..interfaces.contract import ContractInterface
from ..interfaces.transaction import TransactionInterface

class Web3Contract(ContractInterface):
    
    def __init__(self, address:str, abi:List[Dict], transaction:TransactionInterface):
        self.address = address
        self.abi = abi
        self.transaction = transaction
        self.contract = Web3().eth.contract(address=address, abi=abi)
 
    def get_address(self) -> str:
        return self.address

    def call(self, function_name: str, args: list) -> Any:
        data = self.contract.encode_abi(
            abi_element_identifier=function_name,
            args=args
        )
        tx = {"to": self.get_address(), "data": data}
        response = self.transaction.get_blockchain_client().eth_call(tx)

        fn = [e for e in self.abi if e["type"] == "function" and e["name"] == function_name]
        if len(fn) == 0:
            raise ContractError(f"Function {function_name} not found in contract")
        types = [e["type"] for e in fn[0]["outputs"]]
        return Web3().codec.decode(types, bytes.fromhex(response[2:]))

    def execute(self, function_name: str, args: list) -> Dict[str, Any]:
        data = self.contract.encode_abi(
            abi_element_identifier=function_name,
            args=args
        )
        tx = self.transaction.create_transaction(to_address=self.get_address(), data=data)
        response = self.transaction.send_signed_transaction(tx)        
        receipt = self.transaction.get_transaction_receipt(response)
        logs = self.transaction.process_receipt(receipt)
        return {"tx_hash": response, "tx_receipt": logs}
