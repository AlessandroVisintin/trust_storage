# TrustStorageClient

TrustStorageClient is a Python module designed to interact with a Besu blockchain network for document integrity verification. This module provides functionality to add, retrieve, and deprecate document hashes on the blockchain.

## Installation

To use the TrustStorageClient module, you can clone the repository and use pip to install it locally:

```bash
git clone ...
pip install /path/to/trust_storage_client
```

It is recommended to activate a virtual environment before installation to avoid global installation:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate.bat`
pip install /path/to/trust_storage_client
```

## Requirements

The module requires the following dependencies:

- cryptography==43.0.3
- eth-abi==5.1.0
- eth-account==0.13.4
- PyJWT==2.10.0
- requests==2.32.3
- web3==7.5.0

These dependencies are listed in the `requirements.txt` file. Users can install them using the following command:

```bash
pip install --no-cache-dir -r /path/to/trust_storage_client/requirements.txt
```

## Configuration

Before using the module, ensure that the following environment variables are set:

- `BESU_ENDPOINT`: The URL of the Besu blockchain endpoint
- `CONTRACT_ADDR_PATH`: Path to the file containing the smart contract address
- `CONTRACT_JSON_PATH`: Path to the JSON file containing the smart contract ABI
- `CLIENT_PRVKEY_PATH`: Path to the file containing the client's private key
- `CLIENT_PUBKEY_PATH`: Path to the file containing the client's public key

Example configuration:

```bash
export BESU_ENDPOINT=http://127.0.0.1:8545
export CONTRACT_ADDR_PATH=/path/to/contract.address
export CONTRACT_JSON_PATH=/path/to/contract.abi
export CLIENT_PRVKEY_PATH=/path/to/key/.prv
export CLIENT_PUBKEY_PATH=/path/to/key/.pub
```

You can set these environment variables in your shell or include them in a configuration file that you source before running your Python script. Make sure to adjust the paths according to your specific project structure and file locations.

## Usage

### Checking Connectivity

To check connectivity with the BESU node:

```python
from trust_storage_client.besu_client import get_chainid

print("Check connectivity with BESU node:")
chain_id = get_chainid()
print(f"Chain ID: {chain_id}")
```

### Adding a Document

To add a document hash to the blockchain:

```python
from trust_storage_client.besu_client import add_besu

with open("/path/to/your/document.json") as f:
    document_content = f.read()

print("Adding document to blockchain:")
result = add_besu(document_content)
document_hash = result['hash']
print(f"Document hash: {document_hash}")
```

### Retrieving a Document

To check if a document hash exists on the blockchain:

```python
from trust_storage_client.besu_client import get_besu

print("Checking if document exists:")
try:
    exists = get_besu(document_hash)
    print(f"Document exists: {exists}")
except RuntimeError as e:
    print(f"Error: {e}")
```

### Deprecating a Document

To deprecate a document hash on the blockchain:

```python
from trust_storage_client.besu_client import deprecate_besu

print("Deprecating document:")
try:
    success = deprecate_besu(document_hash)
    print(f"Document deprecated successfully: {success}")
except RuntimeError as e:
    print(f"Error: {e}")
```

### Error Handling

The module raises `RuntimeError` for various scenarios. Here's how to handle them:

```python
from trust_storage_client.besu_client import add_besu, get_besu, deprecate_besu

# Trying to add an already existing document
try:
    add_besu(document_content)
except RuntimeError:
    print("Document already exists")

# Trying to get a non-existent document
try:
    get_besu("0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef")
except RuntimeError:
    print("Document does not exist")

# Trying to deprecate an already deprecated document
try:
    deprecate_besu(document_hash)
except RuntimeError:
    print("Document already deprecated")

# Trying to get a deprecated document
try:
    get_besu(document_hash)
except RuntimeError:
    print("Document has been deprecated")
```