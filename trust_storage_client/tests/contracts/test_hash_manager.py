import json
import pytest
from web3 import Web3
from web3.exceptions import Web3RPCError
from eth_account import Account

from trust_storage_client.utils import is_node_responding
from trust_storage_client.contracts.hash_manager import HashManager

@pytest.fixture(scope="session")
def docker_required():
    """Skip tests if Docker container is not available."""
    if not is_node_responding("http://127.0.0.1:8545"):
        pytest.skip("Besu node is not available")

@pytest.fixture(scope="session")
def node_url():
    return "http://127.0.0.1:8545"

@pytest.fixture
def test_private_key():
    """Return a test private key."""
    return "0x3f9d4328d47d5aa8b84c4716679a78fc21eab62be253b99315e4fa924d07559f"

@pytest.fixture
def hash_manager_abi():
    return [{'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'bytes32', 'name': 'hashValue', 'type': 'bytes32'}, {'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}], 'name': 'HashAdded', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'bytes32', 'name': 'hashValue', 'type': 'bytes32'}, {'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}], 'name': 'HashDeprecated', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'bytes32', 'name': 'oldHashValue', 'type': 'bytes32'}, {'indexed': True, 'internalType': 'bytes32', 'name': 'newHashValue', 'type': 'bytes32'}, {'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}], 'name': 'HashUpdated', 'type': 'event'}, {'inputs': [{'internalType': 'bytes32', 'name': '_hash', 'type': 'bytes32'}], 'name': 'add', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'bytes32', 'name': '_hash', 'type': 'bytes32'}], 'name': 'deprecate', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'bytes32', 'name': '_hash', 'type': 'bytes32'}], 'name': 'read', 'outputs': [{'internalType': 'uint256', 'name': 'index', 'type': 'uint256'}, {'internalType': 'address', 'name': 'owner', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}]

@pytest.fixture
def contract_address():
    return "0x000052657363616C65486173684D616e61676572"

@pytest.fixture
def hash_manager(contract_address, hash_manager_abi, node_url):
    """Initialize HashManager with test contract."""
    return HashManager(
        contract_address=contract_address,
        abi=hash_manager_abi,
        node_url=node_url
    )

@pytest.fixture
def test_hash():
    return Web3.keccak(text="test-data")

def test_initial_connection(hash_manager):
    """Test successful connection to Besu node."""
    assert hash_manager.w3.eth.block_number

def test_add_hash(hash_manager, test_private_key, test_hash):
    """Test adding a hash to the contract."""
    receipt = hash_manager.add_hash(test_hash, test_private_key)
    
    if 'error' in receipt:  # Handle error case
        assert "Hash already exists" in receipt['error']['message']
    else:  # Handle success case
        assert receipt['status'] == '1'
        read_result = hash_manager.read_hash(test_hash)
        if isinstance(read_result, dict):  # Error reading
            assert False, f"Read failed: {read_result['error']['message']}"
        else:  # Valid response
            _, owner_address = read_result
            expected_address = Account.from_key(test_private_key).address
            assert owner_address == expected_address

def test_hash_deprecation(hash_manager, test_private_key, test_hash):
    """Test deprecating a hash."""
    receipt = hash_manager.deprecate_hash(test_hash, test_private_key)
    
    if 'error' in receipt:
        assert "Hash does not exist" in receipt['error']['message']
    else:
        assert receipt['status'] == '1'
        read_result = hash_manager.read_hash(test_hash)
        assert isinstance(read_result, dict), "Deprecated hash still exists"


def test_event_logs(hash_manager, test_private_key, test_hash):
    """Test retrieval of event logs."""
    initial_block = hash_manager.w3.eth.block_number
    hash_manager.add_hash(test_hash, test_private_key)
    logs = hash_manager.get_event_logs("HashAdded", from_block=initial_block)
    assert len(logs) > 0, "No events found"
    event_args = logs[0]['args']
    assert event_args['hashValue'] == test_hash, "Hash mismatch in event"
    assert event_args['owner'] == Account.from_key(test_private_key).address, "Owner mismatch"
