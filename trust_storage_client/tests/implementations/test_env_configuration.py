# test_environment_configuration.py

import os
import pytest
from trust_storage_client.interfaces.configuration import ConfigurationInterface
from trust_storage_client.implementations.env_configuration import EnvConfiguration

@pytest.fixture
def mock_env_vars(mocker):
    """Setup mock environment variables for testing."""
    env_vars = {
        'BLOCKCHAIN_ENDPOINT': 'http://test-endpoint.com',
        'CONTRACT_ADDRESS_FILE': '/path/to/contract_address.txt',
        'CONTRACT_ABI_FILE': '/path/to/contract_abi.json',
        'PRIVATE_KEY_FILE': '/path/to/private_key.txt',
        'PUBLIC_KEY_FILE': '/path/to/public_key.txt'
    }
    mocker.patch.dict(os.environ, env_vars)
    return env_vars

@pytest.fixture
def mock_file_reads(mocker, mock_env_vars):
    """Mock file read operations with different content for each file."""
    file_contents = {
        mock_env_vars['CONTRACT_ADDRESS_FILE']: '0x1234567890abcdef',
        mock_env_vars['CONTRACT_ABI_FILE']: '{"some": "abi"}',
        mock_env_vars['PRIVATE_KEY_FILE']: 'private_key_value',
        mock_env_vars['PUBLIC_KEY_FILE']: 'public_key_value'
    }
    
    def mock_open_side_effect(file_path, *args, **kwargs):
        if file_path not in file_contents:
            raise FileNotFoundError(f"File not found: {file_path}")        
        m = mocker.mock_open(read_data=file_contents[file_path])
        return m(file_path, *args, **kwargs)
    mock = mocker.patch('builtins.open', side_effect=mock_open_side_effect)
    return mock, file_contents

def test_environment_configuration_init_success(mock_env_vars, mock_file_reads):
    """Test that EnvConfiguration initializes successfully with valid environment variables."""
    mock_open, file_contents = mock_file_reads
    config = EnvConfiguration()

    assert config.get_endpoint() == mock_env_vars['BLOCKCHAIN_ENDPOINT']
    assert config.get_contract_address() == file_contents[mock_env_vars['CONTRACT_ADDRESS_FILE']]
    assert config.get_contract_abi() == file_contents[mock_env_vars['CONTRACT_ABI_FILE']]
    assert config.get_private_key() == file_contents[mock_env_vars['PRIVATE_KEY_FILE']]
    assert config.get_public_key() == file_contents[mock_env_vars['PUBLIC_KEY_FILE']]

def test_environment_configuration_init_missing_endpoint(mocker):
    """Test that initialization fails when BLOCKCHAIN_ENDPOINT environment variable is missing."""
    mocker.patch.dict(os.environ, {}, clear=True)
    with pytest.raises(ValueError, match="BLOCKCHAIN_ENDPOINT environment variable not set"):
        EnvConfiguration()

@pytest.mark.parametrize("missing_var", [
    'CONTRACT_ADDRESS_FILE',
    'CONTRACT_ABI_FILE',
    'PRIVATE_KEY_FILE',
    'PUBLIC_KEY_FILE'
])
def test_environment_configuration_init_missing_file_env_var(mocker, missing_var):
    """Test that initialization fails when a required file environment variable is missing."""
    # Setup all environment variables except the one being tested
    env_vars = {
        'BLOCKCHAIN_ENDPOINT': 'http://test-endpoint.com',
        'CONTRACT_ADDRESS_FILE': '/path/to/contract_address.txt',
        'CONTRACT_ABI_FILE': '/path/to/contract_abi.json',
        'PRIVATE_KEY_FILE': '/path/to/private_key.txt',
        'PUBLIC_KEY_FILE': '/path/to/public_key.txt'
    }
    
    del env_vars[missing_var]
    
    mocker.patch.dict(os.environ, env_vars, clear=True)
    mocker.patch('builtins.open', mocker.mock_open(read_data="mock content"))
    with pytest.raises(ValueError, match=f"{missing_var} environment variable not set"):
        EnvConfiguration()

def test_environment_configuration_init_file_not_found(mocker):
    """Test that initialization fails when a referenced file doesn't exist."""
    env_vars = {
        'BLOCKCHAIN_ENDPOINT': 'http://test-endpoint.com',
        'CONTRACT_ADDRESS_FILE': '/path/to/nonexistent.txt',
        'CONTRACT_ABI_FILE': '/path/to/contract_abi.json',
        'PRIVATE_KEY_FILE': '/path/to/private_key.txt',
        'PUBLIC_KEY_FILE': '/path/to/public_key.txt'
    }
    mocker.patch.dict(os.environ, env_vars)
    error_message = f"File not found: {env_vars['CONTRACT_ADDRESS_FILE']}"
    mocker.patch('builtins.open', side_effect=FileNotFoundError(error_message))
    with pytest.raises(FileNotFoundError, match=error_message):
        EnvConfiguration()

def test_from_file_success(mocker):
    """Test that _from_file method correctly reads content from a file."""
    test_file_path = '/path/to/test.txt'
    test_content = 'test content'
    mocker.patch.dict(os.environ, {'TEST_FILE': test_file_path})
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=test_content))
    mocker.patch.object(EnvConfiguration, '__init__', return_value=None)
    config = EnvConfiguration()
    result = config._from_file('TEST_FILE')
    
    assert result == test_content
    mock_open.assert_called_once_with(test_file_path, 'r')

def test_from_file_missing_env_var(mocker):
    """Test that _from_file raises ValueError when environment variable is missing."""
    mocker.patch.dict(os.environ, {}, clear=True)
    mocker.patch.object(EnvConfiguration, '__init__', return_value=None)
    config = EnvConfiguration()
    with pytest.raises(ValueError, match="TEST_FILE environment variable not set"):
        config._from_file('TEST_FILE')

def test_from_file_file_not_found(mocker):
    """Test that _from_file raises FileNotFoundError when file doesn't exist."""
    test_file_path = '/path/to/nonexistent.txt'
    error_message = f"File not found: {test_file_path}"    
    mocker.patch.dict(os.environ, {'TEST_FILE': test_file_path})
    mocker.patch('builtins.open', side_effect=FileNotFoundError(error_message))
    mocker.patch.object(EnvConfiguration, '__init__', return_value=None)
    config = EnvConfiguration()
    with pytest.raises(FileNotFoundError, match=f"File not found: {test_file_path}"):
        config._from_file('TEST_FILE')

@pytest.mark.parametrize("method,env_var,file_content", [
    ('get_endpoint', 'BLOCKCHAIN_ENDPOINT', None),
    ('get_contract_address', 'CONTRACT_ADDRESS_FILE', '0x1234567890abcdef'),
    ('get_contract_abi', 'CONTRACT_ABI_FILE', '{"some": "abi"}'),
    ('get_private_key', 'PRIVATE_KEY_FILE', 'private_key_value'),
    ('get_public_key', 'PUBLIC_KEY_FILE', 'public_key_value')
])
def test_getter_methods(mocker, mock_env_vars, mock_file_reads, method, env_var, file_content):
    """Test that all getter methods return the correct values."""
    mock_open, file_contents = mock_file_reads
    config = EnvConfiguration()
    getter_method = getattr(config, method)
    result = getter_method()
    expected = mock_env_vars[env_var] if file_content is None else file_content
    assert result == expected
