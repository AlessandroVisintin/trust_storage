# HashManager Python Client

## Overview

The `HashManager` class is a Python client for interacting with a Hyperledger Besu smart contract that manages a registry of hashes. It allows you to add, read, deprecate (remove), and query logs for hashes stored on-chain. This is useful for building trustable, auditable registries of digital assets, file fingerprints, or any data that can be represented as a `bytes32` hash.

This README explains how to use the `HashManager` class, the structure of its JSON responses, and the possible error messages you may encounter, based on the smart contract logic.

---

## Table of Contents

- [Usage](#usage)
  - [Adding a Hash](#adding-a-hash)
  - [Reading a Hash](#reading-a-hash)
  - [Deprecating a Hash](#deprecating-a-hash)
  - [Retrieving Event Logs](#retrieving-event-logs)
- [JSON Output Structure](#json-output-structure)
- [Error Messages](#error-messages)
- [Event Log Structure](#event-log-structure)

---

## Installation

Ensure you have the following dependencies installed:

```bash
pip install web3 eth-account pytest
```

The `HashManager` class also depends on a utility function `to_0xhex` and a running Besu node.

---

## Initialization

To use the `HashManager`, you need:

- The deployed contract address (`contract_address`)
- The contract ABI (`abi`)
- The Besu node HTTP URL (`node_url`)

```python
from trust_storage_client.contracts.hash_manager import HashManager

contract_address = "0x000052657363616C65486173684D616e61676572"  # Example address
abi = [...]  # Contract ABI as a Python list/dict
node_url = "http://127.0.0.1:8545"

hash_manager = HashManager(contract_address, abi, node_url)
```

---

## Usage

### Adding a Hash

```python
data_hash = Web3.keccak(text="my-data")  # bytes32 hash
private_key = "0x..."  # Owner's private key

receipt = hash_manager.add_hash(data_hash, private_key)
print(receipt)
```

#### **Success Response Example**

```json
{
  "status": "1",
  "block": {
    "hash": "0x997be2e3c5f0a99452220a69e64d3e195ac31d8df8d6b060eca7cb272c6a28e4",
    "number": 3734
  },
  "transaction": {
    "hash": "0x5ce89d6dcf821c63dd980226f23d2480aa3fd7cef084cefcfea53e59d953f914",
    "from": "0x31172360E655f0161Aec14925E2223F60414Bb81",
    "to": "0x000052657363616C65486173684D616e61676572",
    "gasUsed": 95535
  },
  "event": {
    "addedHash": "0xf3574bbaa01629ebe07e14d07750f784439c00b7d515f3589c66e739df197aea"
  }
}
```

#### **Error Example**

```json
{
  "error": {
    "code": -32000,
    "message": "Execution reverted: Hash already exists",
    "data": "0x08c379a0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000134861736820616c7265616479206578697374730000000000000000000000000000"
  }
}
```

---

### Reading a Hash

```python
result = hash_manager.read_hash(data_hash)
print(result)
```

#### **Success Response**

A list: `[index, owner_address]`

```python
[5, "0x31172360E655f0161Aec14925E2223F60414Bb81"]
```

#### **Error Example**

```json
{
  "error": {
    "code": -32000,
    "message": "Execution reverted: Hash does not exist",
    "data": "0x08c379a0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000134861736820646f6573206e6f7420657869737400000000000000000000000000"
  }
}
```

---

### Deprecating a Hash

```python
receipt = hash_manager.deprecate_hash(data_hash, private_key)
print(receipt)
```

#### **Success Response Example**

```json
{
  "status": "1",
  "block": {
    "hash": "0x19e1a0fcc0ba90ea00a0c3100dec7e9905d5cbed6bde1793113cdc92e76b19d0",
    "number": 3735
  },
  "transaction": {
    "hash": "0x9f2b6afbbae2c71fd09b5af16dd90dc0a13418819297c4862f486cd04d4d9c01",
    "from": "0x31172360E655f0161Aec14925E2223F60414Bb81",
    "to": "0x000052657363616C65486173684D616e61676572",
    "gasUsed": 35750
  },
  "event": {
    "deprecatedHash": "0xf3574bbaa01629ebe07e14d07750f784439c00b7d515f3589c66e739df197aea"
  }
}
```

#### **Error Example**

```json
{
  "error": {
    "code": -32000,
    "message": "Execution reverted: Caller is not the owner",
    "data": "0x08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000001843616c6c6572206973206e6f7420746865206f776e6572000000000000000000"
  }
}
```

---

### Retrieving Event Logs

```python
logs = hash_manager.get_event_logs("HashAdded", from_block=0)
for log in logs:
    print(log['args'])
```

#### **Event Log Example**

```python
{
  'hashValue': b'\xf3WK\xba\xa0\x16)\xeb\xe0~\x14\xd0wP\xf7\x84C\x9c\x00\xb7\xd5\x15\xf3X\x9cf\xe79\xdf\x19z\xea',  # bytes32 hash
  'owner': '0x31172360E655f0161Aec14925E2223F60414Bb81'  # address of the owner
}
```

---

## JSON Output Structure

### On Success

- **status**: `"1"` (string, indicates success)
- **block**: 
  - `hash`: Block hash (hex string)
  - `number`: Block number (integer)
- **transaction**: 
  - `hash`: Transaction hash (hex string)
  - `from`: Sender address
  - `to`: Contract address
  - `gasUsed`: Gas consumed (integer)
- **event**: 
  - `addedHash` (for `add_hash`) or `deprecatedHash` (for `deprecate_hash`): The hash involved (hex string)

### On Error

- **error**: 
  - `code`: RPC error code (integer)
  - `message`: Full error message including "Execution reverted: " prefix
  - `data`: Raw revert data (hex string)

---

## Error Messages

Errors returned by the smart contract include:

- `"Execution reverted: Hash already exists"`
- `"Execution reverted: Invalid hash"`
- `"Execution reverted: Hash does not exist"`
- `"Execution reverted: Caller is not the owner"`

These are returned in the `message` field of the error object, prefixed with `Execution reverted: `.

---

## Event Log Structure

Event logs are returned as a list of dictionaries. Each log contains:

- `args`: Event parameters (e.g., `hashValue`, `owner`)
- Other metadata (block number, transaction hash, etc.)

Example for `HashAdded`:
```python
{
  'args': {
    'hashValue': b'\xf3W...',  # bytes32
    'owner': '0x3117...'       # address
  },
  'event': 'HashAdded',
  ...
}
```

---

## Testing

Tests use `pytest` and require a running Besu node. Key test scenarios:
- Successful hash addition/read/deprecation
- Error handling for duplicate hashes, invalid ownership, etc.
- Event log retrieval

---

## Example Workflow

```python
from web3 import Web3
from trust_storage_client.contracts.hash_manager import HashManager

# Setup
contract_address = "0x000052657363616C65486173684D616e61676572"
abi = [...]  # Your contract ABI
node_url = "http://127.0.0.1:8545"
private_key = "0x3f9d4328d47d5aa8b84c4716679a78fc21eab62be253b99315e4fa924d07559f"

hash_manager = HashManager(contract_address, abi, node_url)

# Add a hash
data_hash = Web3.keccak(text="example-data")
add_result = hash_manager.add_hash(data_hash, private_key)
print(add_result)  # Expect structure like the "add_hash" example above

# Read the hash
read_result = hash_manager.read_hash(data_hash)
print(read_result)  # Expect format [index, owner_address]

# Deprecate the hash
deprecate_result = hash_manager.deprecate_hash(data_hash, private_key)
print(deprecate_result)  # Expect structure like the "deprecate_hash" example

# Get event logs
logs = hash_manager.get_event_logs("HashAdded", from_block=0)
for log in logs:
    print(log['args'])  # Expect hashValue and owner details
```