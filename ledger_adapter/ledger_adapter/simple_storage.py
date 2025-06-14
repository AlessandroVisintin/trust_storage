import ast
from typing import Dict, Any

from .base_contract import BaseContract
# from web3 import Web3
from web3.exceptions import Web3RPCError
# from web3.middleware import ExtraDataToPOAMiddleware
from eth_account import Account


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
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            logs = self.contract.events.DataChanged().process_receipt(receipt)
            event_data = logs[0]['args'] if logs else {}

            print(receipt, end="\n\n")
            print(logs, end="\n\n")
            print(event_data, end="\n\n")

            # return {
            #     "status": str(receipt.get('status')),
            #     "block": {
            #         "hash": to_0xhex(receipt.get('blockHash')),
            #         "number": receipt.get('blockNumber')
            #     },
            #     "transaction": {
            #         "hash": to_0xhex(receipt.get('transactionHash')),
            #         "from": receipt.get('from'),
            #         "to": receipt.get('to'),
            #         "gasUsed": receipt.get('gasUsed')
            #     },
            #     "event": {
            #         "oldValue": event_data.get('oldValue'),
            #         "newValue": event_data.get('newValue'),
            #         "changer": event_data.get('changer')
            #     }
            # }
        except Web3RPCError as e:
            try:
                error_message = ast.literal_eval(e.message)
            except (ValueError, SyntaxError):
                error_message = str(e)
            return {'error': error_message}
        except Exception as e:
            return {'error': str(e)}

    def get_data(self) -> str:
        try:
            return self.contract.functions.get().call()
        except Exception as e:
            return {'error': str(e)}
