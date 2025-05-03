import sys
import json
from pathlib import Path

from trust_storage_client.config_manager import ConfigManager
from trust_storage_client.implementations.http_blockchain import HttpBlockchainClient
from trust_storage_client.trust_storage_client.implementations.web3_transaction import BesuTransaction
from trust_storage_client.implementations.web3_contract import Web3Contract
from trust_storage_client.clients.hash_manager_client import HashManagerClient

def main():

    parent_dir = Path(__file__).parent.absolute()

    config_file = parent_dir / "config.json"
    config = ConfigManager(config_file=config_file)
    
    print(f"Using config file at: {config_file}")
    print(f"Using Besu node at: {config.get_endpoint()}")

    with open(parent_dir / config.get_contract_address(), 'r') as f:
        contract_address = f.read()
    with open(parent_dir / config.get_contract_abi(), 'r') as f:
        contract_abi = f.read()
    contract = Web3Contract(contract_address, contract_abi)
 
    print(f"Using contract at: {contract_address}")
    
    blockchain_client = HttpBlockchainClient(config.get_endpoint())
    transaction = BesuTransaction(blockchain_client)
    
    
    # # Create HashManager client
    # hash_manager = HashManagerClient(
    #     blockchain_client=blockchain_client,
    #     contract=contract,
    #     transaction=transaction,
    #     private_key=config_manager.get_private_key(),
    #     public_key=config_manager.get_public_key()
    # )
    
    # # Test document operations
    # test_document = "This is a test document to be added to the blockchain"
    
    # # Add document
    # print("\nAdding document to blockchain...")
    # try:
    #     result = hash_manager.add_document(test_document)
    #     doc_hash = result.get("args", {}).get("hash", "Unknown")
    #     print(f"Document added successfully with hash: {doc_hash}")
    # except Exception as e:
    #     print(f"Error adding document: {str(e)}")
    #     return
    
    # # Verify document exists
    # print("\nVerifying document exists...")
    # try:
    #     exists = hash_manager.get_document(doc_hash)
    #     print(f"Document verification result: {'Exists' if exists else 'Not found'}")
    # except Exception as e:
    #     print(f"Error verifying document: {str(e)}")
    
    # # Deprecate document
    # print("\nDeprecating document...")
    # try:
    #     deprecated = hash_manager.deprecate_document(doc_hash)
    #     print(f"Document deprecation result: {'Success' if deprecated else 'Failed'}")
    # except Exception as e:
    #     print(f"Error deprecating document: {str(e)}")

if __name__ == "__main__":
    main()
