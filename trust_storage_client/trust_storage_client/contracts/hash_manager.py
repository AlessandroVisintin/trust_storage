import json
import ast

from web3 import Web3
from web3.exceptions import Web3RPCError
from web3.middleware import ExtraDataToPOAMiddleware
from eth_account import Account

from ..utils import to_0xhex

class HashManager:
    def __init__(self, contract_address, abi, node_url="http://127.0.0.1:8545"):
        """
        Initialize interface with Hyperledger Besu node
        :param contract_address: Deployed contract address
        :param abi: Contract ABI
        :param node_url: Besu node URL (default: localhost)
        """
        self.w3 = Web3(Web3.HTTPProvider(node_url))
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        self.contract = self.w3.eth.contract(
            address=contract_address,
            abi=abi
        )
        
    def add_hash(self, data_hash, private_key):
        """
        Add a new hash to the contract
        :param data_hash: Bytes32 hash to store
        :param private_key: Owner's private key
        :return: Transaction receipt
        """        
        try:
            account = Account.from_key(private_key)
            nonce = self.w3.eth.get_transaction_count(account.address)
            gas_estimate = self.contract.functions.add(data_hash).estimate_gas({
                'from': account.address
            })
            
            tx = self.contract.functions.add(data_hash).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': int(gas_estimate * 1.2),
                'gasPrice': 0,    # Free gas for local networks
                'nonce': nonce,
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            raw = dict(receipt)
            log = receipt['logs'][0] if receipt['logs'] else {}
            topics = log.get('topics', [])

            return {
                "status": str(raw['status']),
                "block": {
                    "hash": to_0xhex(raw['blockHash']),
                    "number": raw['blockNumber']
                },
                "transaction": {
                    "hash": to_0xhex(raw['transactionHash']),
                    "from": raw['from'],
                    "to": raw['to'],
                    "gasUsed": raw['gasUsed']
                },
                "event": {
                    "addedHash": to_0xhex(topics[1])
                }
            }
        except Web3RPCError as e:
            return { 'error': ast.literal_eval( e.message ) }

    def read_hash(self, data_hash):
        """
        Retrieve hash information from contract
        :param data_hash: Bytes32 hash to lookup
        :return: (index, owner) tuple
        """
        try:
            return self.contract.functions.read(data_hash).call()
        except Web3RPCError as e:
            return { 'error': ast.literal_eval( e.message ) }
    
    def deprecate_hash(self, data_hash, private_key):
        """
        Remove a hash from the contract
        :param data_hash: Bytes32 hash to remove
        :param private_key: Owner's private key
        :return: Transaction receipt
        """
        try:
            account = Account.from_key(private_key)
            nonce = self.w3.eth.get_transaction_count(account.address)
            gas_estimate = self.contract.functions.deprecate(data_hash).estimate_gas({
                'from': account.address
            })
            
            tx = self.contract.functions.deprecate(data_hash).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': int(gas_estimate * 1.2),
                'gasPrice': 0,
                'nonce': nonce,
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            raw = dict(receipt)
            log = receipt['logs'][0] if receipt['logs'] else {}
            topics = log.get('topics', [])
            return {
                "status": str(raw['status']),
                "block": {
                    "hash": to_0xhex(raw['blockHash']),
                    "number": raw['blockNumber']
                },
                "transaction": {
                    "hash": to_0xhex(raw['transactionHash']),
                    "from": raw['from'],
                    "to": raw['to'],
                    "gasUsed": raw['gasUsed']
                },
                "event": {
                    "deprecatedHash": to_0xhex(topics[1])
                }
            }
        except Web3RPCError as e:
            return { 'error': ast.literal_eval( e.message ) }
        

    def get_event_logs(self, event_name, from_block=0):
        """
        Get contract event logs
        :param event_name: Name of the event (HashAdded/HashUpdated/HashDeprecated)
        :param from_block: Starting block number
        :return: List of event logs
        """
        event = getattr(self.contract.events, event_name)
        return event.get_logs(from_block=from_block)
