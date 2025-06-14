import ast
from typing import Dict, Any

from web3.exceptions import Web3RPCError 
from eth_account import Account

from .base_contract import BaseContract
from .adapter_utils import (
    parse_response_from_receipt, send_and_wait_transaction,
    parse_error
)


class SimpleStorage(BaseContract):

    def set_data(self, new_value: str, private_key: str) -> Dict[str, Any]:
        try:
            account = Account.from_key(private_key)
            nonce = self.w3.eth.get_transaction_count(account.address)
            tx_params = {
                'from': account.address,
                'chainId': self.w3.eth.chain_id,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            }
            gas_estimate = self.contract.functions.set(new_value).estimate_gas(tx_params)
            tx_params['gas'] = int(gas_estimate * 1.2)
            tx = self.contract.functions.set(new_value).build_transaction(tx_params)
            receipt = send_and_wait_transaction(self.w3, tx, private_key)
            return parse_response_from_receipt(self.contract, receipt)

        except Web3RPCError as e:
            return parse_error(e)

        #     try:
        #         error_message = ast.literal_eval(e.message)
        #     except (ValueError, SyntaxError):
        #         error_message = str(e)
        #     return {'error': error_message}
        # except Exception as e:
        #     return {'error': str(e)}

    def get_data(self) -> str:
        try:
            return self.contract.functions.get().call()
        except Exception as e:
            return {'error': str(e)}
