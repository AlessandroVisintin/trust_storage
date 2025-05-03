# test_web3_contract.py

import pytest
from web3 import Web3

from trust_storage_client.utils import is_node_responding
from trust_storage_client.implementations.web3_transaction import Web3Transaction
from trust_storage_client.implementations.http_blockchain import HttpBlockchainClient
from trust_storage_client.implementations.web3_contract import Web3Contract

# Docker integration test fixtures
@pytest.fixture
def test_private_key():
    """Return a test private key."""
    return "0x3f9d4328d47d5aa8b84c4716679a78fc21eab62be253b99315e4fa924d07559f"

@pytest.fixture
def blockchain_client():
    """Fixture for a local blockchain client connecting to Docker container."""
    return HttpBlockchainClient("http://127.0.0.1:8545")

@pytest.fixture(scope="session")
def docker_required():
    """Skip tests if Docker container is not available."""
    if not is_node_responding("http://127.0.0.1:8545"):
        pytest.skip("Besu node is not available")

@pytest.fixture
def simple_storage_bytecode():
    """Bytecode for the SimpleStorage contract."""
    return "0x608060405234801561000f575f80fd5b506040518060400160405280600d81526020017f496e697469616c2056616c7565000000000000000000000000000000000000008152505f90816100539190610293565b50610362565b5f81519050919050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52604160045260245ffd5b7f4e487b71000000000000000000000000000000000000000000000000000000005f52602260045260245ffd5b5f60028204905060018216806100d457607f821691505b6020821081036100e7576100e6610090565b5b50919050565b5f819050815f5260205f209050919050565b5f6020601f8301049050919050565b5f82821b905092915050565b5f600883026101497fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8261010e565b610153868361010e565b95508019841693508086168417925050509392505050565b5f819050919050565b5f819050919050565b5f61019761019261018d8461016b565b610174565b61016b565b9050919050565b5f819050919050565b6101b08361017d565b6101c46101bc8261019e565b84845461011a565b825550505050565b5f90565b6101d86101cc565b6101e38184846101a7565b505050565b5b81811015610206576101fb5f826101d0565b6001810190506101e9565b5050565b601f82111561024b5761021c816100ed565b610225846100ff565b81016020851015610234578190505b610248610240856100ff565b8301826101e8565b50505b505050565b5f82821c905092915050565b5f61026b5f1984600802610250565b1980831691505092915050565b5f610283838361025c565b9150826002028217905092915050565b61029c82610059565b67ffffffffffffffff8111156102b5576102b4610063565b5b6102bf82546100bd565b6102ca82828561020a565b5f60209050601f8311600181146102fb575f84156102e9578287015190505b6102f38582610278565b86555061035a565b601f198416610309866100ed565b5f5b828110156103305784890151825560018201915060208501945060208101905061030b565b8683101561034d5784890151610349601f89168261025c565b8355505b6001600288020188555050505b505050505050565b6107118061036f5f395ff3fe608060405234801561000f575f80fd5b506004361061004a575f3560e01c80632a1afcd91461004e5780634ed3885e1461006c5780636d4ce63c1461008857806383197ef0146100a6575b5f80fd5b6100566100b0565b6040516100639190610265565b60405180910390f35b610086600480360381019061008191906103c2565b61013b565b005b61009061014d565b60405161009d9190610265565b60405180910390f35b6100ae6101dc565b005b5f80546100bc90610436565b80601f01602080910402602001604051908101604052809291908181526020018280546100e890610436565b80156101335780601f1061010a57610100808354040283529160200191610133565b820191905f5260205f20905b81548152906001019060200180831161011657829003601f168201915b505050505081565b805f9081610149919061060c565b5050565b60605f805461015b90610436565b80601f016020809104026020016040519081016040528092919081815260200182805461018790610436565b80156101d25780601f106101a9576101008083540402835291602001916101d2565b820191905f5260205f20905b8154815290600101906020018083116101b557829003601f168201915b5050505050905090565b3373ffffffffffffffffffffffffffffffffffffffff16ff5b5f81519050919050565b5f82825260208201905092915050565b8281835e5f83830152505050565b5f601f19601f8301169050919050565b5f610237826101f5565b61024181856101ff565b935061025181856020860161020f565b61025a8161021d565b840191505092915050565b5f6020820190508181035f83015261027d818461022d565b905092915050565b5f604051905090565b5f80fd5b5f80fd5b5f80fd5b5f80fd5b7f4e487b71000000000000000000000000000000000000000000000000000000005f52604160045260245ffd5b6102d48261021d565b810181811067ffffffffffffffff821117156102f3576102f261029e565b5b80604052505050565b5f610305610285565b905061031182826102cb565b919050565b5f67ffffffffffffffff8211156103305761032f61029e565b5b6103398261021d565b9050602081019050919050565b828183375f83830152505050565b5f61036661036184610316565b6102fc565b9050828152602081018484840111156103825761038161029a565b5b61038d848285610346565b509392505050565b5f82601f8301126103a9576103a8610296565b5b81356103b9848260208601610354565b91505092915050565b5f602082840312156103d7576103d661028e565b5b5f82013567ffffffffffffffff8111156103f4576103f3610292565b5b61040084828501610395565b91505092915050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52602260045260245ffd5b5f600282049050600182168061044d57607f821691505b6020821081036104605761045f610409565b5b50919050565b5f819050815f5260205f209050919050565b5f6020601f8301049050919050565b5f82821b905092915050565b5f600883026104c27fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82610487565b6104cc8683610487565b95508019841693508086168417925050509392505050565b5f819050919050565b5f819050919050565b5f61051061050b610506846104e4565b6104ed565b6104e4565b9050919050565b5f819050919050565b610529836104f6565b61053d61053582610517565b848454610493565b825550505050565b5f90565b610551610545565b61055c818484610520565b505050565b5b8181101561057f576105745f82610549565b600181019050610562565b5050565b601f8211156105c45761059581610466565b61059e84610478565b810160208510156105ad578190505b6105c16105b985610478565b830182610561565b50505b505050565b5f82821c905092915050565b5f6105e45f19846008026105c9565b1980831691505092915050565b5f6105fc83836105d5565b9150826002028217905092915050565b610615826101f5565b67ffffffffffffffff81111561062e5761062d61029e565b5b6106388254610436565b610643828285610583565b5f60209050601f831160018114610674575f8415610662578287015190505b61066c85826105f1565b8655506106d3565b601f19841661068286610466565b5f5b828110156106a957848901518255600182019150602085019450602081019050610684565b868310156106c657848901516106c2601f8916826105d5565b8355505b6001600288020188555050505b50505050505056fea26469706673582212207c4c5363e446c4a48f0eab06a333df8ca5fb3a521aa1c9387af610d90940959764736f6c634300081a0033"

@pytest.fixture
def simple_storage_abi():
    return [{"inputs": [],"name": "destroy","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "string","name": "newValue","type": "string"}],"name": "set","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"stateMutability": "nonpayable","type": "constructor"},{"inputs": [],"name": "get","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "storedData","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"}]

# Docker Integration Tests
class TestDockerIntegration:
    """Integration tests for Web3Contract using a Docker-based Ethereum node."""
    
    contract_address = None
    
    def test_deploy_simple_storage_contract(self, docker_required, simple_storage_bytecode, 
                                           blockchain_client, test_private_key):
        """Test deploying the SimpleStorage contract and creating a Web3Contract instance."""
        transaction = Web3Transaction(blockchain_client, test_private_key)
        tx = transaction.create_transaction(to_address=None, data=simple_storage_bytecode)
        try:
            response = transaction.send_signed_transaction(tx)
            receipt = transaction.get_transaction_receipt(response, retry=20, interval=1)
            assert receipt["status"] == "0x1", "Contract deployment failed"
            assert "contractAddress" in receipt, "No contract address in receipt"
            TestDockerIntegration.contract_address = Web3.to_checksum_address(receipt["contractAddress"])
        except Exception as e:
            if "Upfront cost exceeds account balance" in str(e):
                pytest.skip("Insufficient funds to deploy contract")
            else:
                pytest.fail(f"Failed to deploy contract: {str(e)}")
    
    def test_create_contract_instance(self, docker_required, simple_storage_abi, 
                                     blockchain_client, test_private_key):
        """Test creating a Web3Contract instance for the deployed contract."""
        if not TestDockerIntegration.contract_address:
            pytest.skip("No contract has been deployed")
        transaction = Web3Transaction(blockchain_client, test_private_key)
        contract = Web3Contract(
            address=TestDockerIntegration.contract_address,
            abi=simple_storage_abi,
            transaction=transaction
        )
        assert contract.address == TestDockerIntegration.contract_address
        assert contract.abi == simple_storage_abi
        assert contract.transaction == transaction
        
    def test_call_contract_read_function(self, docker_required, simple_storage_abi, 
                                        blockchain_client, test_private_key):
        """Test calling a read-only contract function using Web3Contract."""
        if not TestDockerIntegration.contract_address:
            pytest.skip("No contract has been deployed")
        transaction = Web3Transaction(blockchain_client, test_private_key)
        contract = Web3Contract(
            address=TestDockerIntegration.contract_address,
            abi=simple_storage_abi,
            transaction=transaction
        )
        result = contract.call(function_name="get", args=[])
        assert "Initial Value" in str(result[0])

    def test_execute_contract_write_function(self, docker_required, simple_storage_abi, 
                                            blockchain_client, test_private_key):
        """Test executing a state-changing contract function using Web3Contract."""
        if not TestDockerIntegration.contract_address:
            pytest.skip("No contract has been deployed")
        transaction = Web3Transaction(blockchain_client, test_private_key)
        contract = Web3Contract(
            address=TestDockerIntegration.contract_address,
            abi=simple_storage_abi,
            transaction=transaction
        )
        new_value = "Updated Contract Value"
        try:
            result = contract.execute(function_name="set", args=[new_value])
            assert "tx_hash" in result
            assert "tx_receipt" in result
            
            updated_value = contract.call(function_name="get", args=[])
            assert new_value in str(updated_value[0])
        except Exception as e:
            if "Upfront cost exceeds account balance" in str(e):
                pytest.skip("Insufficient funds for contract interaction")
            else:
                pytest.fail(f"Failed to execute contract function: {str(e)}")

    def test_contract_error_handling(self, docker_required, simple_storage_abi, 
                                    blockchain_client, test_private_key):
        """Test error handling when contract execution fails."""
        # Skip if we don't have a contract address
        if not TestDockerIntegration.contract_address:
            pytest.skip("No contract has been deployed")
        
        invalid_private_key = "0x0000000000000000000000000000000000000000000000000000000000000000"
        transaction = Web3Transaction(blockchain_client, invalid_private_key)
        contract = Web3Contract(
            address=TestDockerIntegration.contract_address,
            abi=simple_storage_abi,
            transaction=transaction
        )
        with pytest.raises(Exception) as excinfo:
            contract.execute(function_name="set", args=["Should Fail"])
        error_msg = str(excinfo.value)
        assert (
            "private key" in error_msg.lower() or
            "account" in error_msg.lower() or
            "signature" in error_msg.lower()
        )
