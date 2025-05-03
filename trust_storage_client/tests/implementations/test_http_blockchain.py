import pytest
import json
import requests
from unittest.mock import Mock, patch

from trust_storage_client.utils import is_node_responding
from trust_storage_client.interfaces.blockchain import BlockchainInterface
from trust_storage_client.implementations.http_blockchain import HttpBlockchainClient
from trust_storage_client.exceptions import BlockchainError


@pytest.fixture
def blockchain_client():
    return HttpBlockchainClient("http://mock-besu-endpoint.com")

@pytest.fixture
def local_client():
    return HttpBlockchainClient("http://127.0.0.1:8545")

@pytest.fixture(scope="session")
def docker_required():
    if not is_node_responding("http://127.0.0.1:8545"):
        pytest.skip("Besu node is not available")

def test_http_blockchain_client_init():
    """Test that constructor correctly sets endpoint and headers."""
    endpoint = "https://test-endpoint.com"
    client = HttpBlockchainClient(endpoint)
    assert client.endpoint == endpoint
    assert client.headers == {"Content-Type": "application/json"}

def test_post_request_success(blockchain_client, mocker):
    """Test that post_request handles successful responses correctly."""
    expected_result = "0x123"
    mock_response = mocker.MagicMock()
    mock_response.content = json.dumps({"result": expected_result})
    mocker.patch("requests.post", return_value=mock_response)
    test_data = {"test": "data"}
    result = blockchain_client.post_request(test_data)
    requests.post.assert_called_once_with(
        blockchain_client.endpoint,
        headers=blockchain_client.headers,
        data=json.dumps(test_data)
    )
    assert result == expected_result

@pytest.mark.parametrize("exception_class,exception_msg", [
    (requests.exceptions.ConnectionError, "Connection refused"),
    (requests.exceptions.Timeout, "Request timed out"),
    (requests.exceptions.HTTPError, "404 Client Error"),
])
def test_post_request_request_exceptions(blockchain_client, mocker, exception_class, exception_msg):
    """Test that post_request properly handles different request exceptions."""
    mock_response = mocker.MagicMock()
    if exception_class == requests.exceptions.HTTPError:
        mock_response.raise_for_status.side_effect = exception_class(exception_msg)
        mocker.patch("requests.post", return_value=mock_response)
    else:
        mocker.patch("requests.post", side_effect=exception_class(exception_msg))    
    with pytest.raises(BlockchainError) as excinfo:
        blockchain_client.post_request({"test": "data"})
    assert "Failed to communicate with blockchain" in str(excinfo.value)
    assert exception_msg in str(excinfo.value)

def test_post_request_error_in_response(blockchain_client, mocker):
    """Test that post_request handles error responses from blockchain."""
    error_message = "Invalid method"
    mock_response = mocker.MagicMock()
    mock_response.content = json.dumps({"error": {"message": error_message}})
    mocker.patch("requests.post", return_value=mock_response)
    with pytest.raises(BlockchainError) as excinfo:
        blockchain_client.post_request({"test": "data"})    
    assert error_message in str(excinfo.value)

def test_post_request_unexpected_format(blockchain_client, mocker):
    """Test that post_request handles unexpected response formats."""
    unexpected_content = {"unexpected": "format"}
    mock_response = mocker.MagicMock()
    mock_response.content = json.dumps(unexpected_content)
    mocker.patch("requests.post", return_value=mock_response)
    with pytest.raises(BlockchainError) as excinfo:
        blockchain_client.post_request({"test": "data"})
    assert "Unexpected response format" in str(excinfo.value)

def test_eth_call_constructs_correct_request(blockchain_client, mocker):
    """Test that eth_call constructs the correct JSON-RPC request."""
    mock_post_request = mocker.patch.object(blockchain_client, "post_request", return_value="0xresult")
    tx = {"to": "0xaddress", "data": "0xdata"}
    block = "latest"
    result = blockchain_client.eth_call(tx, block)
    expected_data = {
        "jsonrpc": "2.0", 
        "method": "eth_call", 
        "params": [tx, block], 
        "id": 53
    }
    mock_post_request.assert_called_once_with(expected_data)
    assert result == "0xresult"

def test_get_nonce_constructs_correct_request(blockchain_client, mocker):
    """Test that get_nonce constructs the correct JSON-RPC request."""
    mock_post_request = mocker.patch.object(blockchain_client, "post_request", return_value="0x1")
    address = "0xaddress"
    result = blockchain_client.get_nonce(address)
    expected_data = {
        "jsonrpc": "2.0", 
        "method": "eth_getTransactionCount", 
        "params": [address, "pending"], 
        "id": 1
    }
    mock_post_request.assert_called_once_with(expected_data)
    assert result == "0x1"

def test_get_chain_id_constructs_correct_request(blockchain_client, mocker):
    """Test that get_chain_id constructs the correct JSON-RPC request."""
    mock_post_request = mocker.patch.object(blockchain_client, "post_request", return_value=1)
    result = blockchain_client.get_chain_id()
    expected_data = {
        "jsonrpc": "2.0", 
        "method": "eth_chainId", 
        "params": [], 
        "id": 51
    }
    mock_post_request.assert_called_once_with(expected_data)
    assert result == 1

## Integration Tests with Docker
def test_integration_post_request_success(docker_required, local_client):
    """Test that post_request works with a real blockchain node."""
    test_data = {"jsonrpc": "2.0", "method": "net_version", "params": [], "id": 1}
    result = local_client.post_request(test_data)
    assert isinstance(result, str)  # Should return a network ID as string

def test_integration_get_chain_id(docker_required, local_client):
    """Test that get_chain_id works with a real blockchain node."""
    chain_id = local_client.get_chain_id()
    assert isinstance(chain_id, (int, str))  # Chain ID could be returned as int or hex string

def test_integration_eth_call(docker_required, local_client):
    """Test that eth_call works with a real blockchain node."""
    tx = {
        "to": "0x0000000000000000000000000000000000000000",  # Replace with actual contract
        "data": "0x18160ddd"  # totalSupply() function signature
    }
    try:
        result = local_client.eth_call(tx)
        assert isinstance(result, str)
    except BlockchainError as e:
        assert "execution reverted" in str(e) or "invalid opcode" in str(e)

def test_integration_get_nonce(docker_required, local_client):
    """Test that get_nonce works with a real blockchain node."""
    address = "0x0000000000000000000000000000000000000000"
    nonce = local_client.get_nonce(address)
    assert isinstance(nonce, str)
    assert nonce.startswith("0x")
