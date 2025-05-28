# QBFT Genesis Creator
**Generate Ethereum genesis.json files for QBFT consensus networks from validator addresses, bootnodes, and smart contracts.**

## Overview
This tool creates production-ready genesis.json files for Ethereum networks using QBFT (Istanbul BFT 2.0) consensus mechanism. It processes validator addresses, bootnode configurations, and smart contract bytecode to generate a complete network initialization file with proper extraData encoding and contract allocations. The tool is containerized for consistent execution across different environments and supports automated configuration through shell scripts that read from configuration files to set up the required data structure.

## Prerequisites
- Docker and Docker Compose installed
- Configuration file (`run.conf`) with proper formatting
- Contract bytecode files (*.bin-runtime format)
- Validator node directories containing `.address` files  
- Bootnode directories containing `.pub` files
- Rust toolchain (optional, for local development)
- Template configuration file (`template.json`)

## Usage
1. Create a `run.conf` configuration file with the proper format (see File Structure section)
2. Run the platform-specific script:
   - **Windows**: Execute `docker/run.bat` (manual data folder setup required)
   - **Linux/Mac**: Execute `docker/run.sh --config run.conf` (automatically generates data folder)
3. The script will automatically create the `data/` directory structure and populate it from your configuration
4. Retrieve the generated `genesis.json` from the `build/` directory
5. Use the genesis file to initialize your QBFT Ethereum network

## File Structure

**Configuration file format (`run.conf`)**:
```
contracts=/path/to/contract1,/path/to/contract2,/path/to/contract3
validators=/path/to/validator1,/path/to/validator2,/path/to/validator3
bootnodes=/path/to/bootnode1,/path/to/bootnode2
```

**Configuration file rules**:
- Use `key=value` format with no spaces around the equals sign
- Separate multiple paths with commas (no spaces)
- Comments start with `#` and empty lines are ignored
- Supported keys:
  - `contracts`: Comma-separated paths to contract files (without .bin-runtime extension)
  - `validators`: Comma-separated paths to validator node directories (containing .address files)
  - `bootnodes`: Comma-separated paths to bootnode directories (containing .pub files)

**Expected directory structure for nodes**:
```
validator1/
└── .address          # Contains validator Ethereum address

bootnode1/
└── .pub              # Contains bootnode public key

contracts/
├── contract1.bin-runtime
├── contract2.bin-runtime
└── contract3.bin-runtime
```

**Auto-generated data structure**:
```
data/
├── validators.txt          # Generated from validator/.address files
├── bootnodes.txt          # Generated from bootnode/.pub files (with @placeholder suffix)
└── contracts/             # Copied contract bytecode files
    ├── contract1.bin-runtime
    ├── contract2.bin-runtime
    └── ...

build/
└── genesis.json           # Generated output file
```

## How It Works
1. **Configuration Reading**: Parses the `run.conf` file to locate contract, validator, and bootnode directories
2. **Data Folder Generation**: Automatically creates and populates the `data/` directory structure from specified paths
3. **Template Loading**: Reads the base genesis configuration from `template.json` with QBFT consensus parameters
4. **Validator Processing**: Reads addresses from `.address` files and encodes them into RLP-formatted extraData field required by QBFT
5. **Bootnode Generation**: Reads public keys from `.pub` files and converts them into enode URLs for network discovery
6. **Contract Allocation**: Copies contract bytecode files, calculates deterministic addresses using "Rescale{contract_name}" prefix, and includes their bytecode
7. **Genesis Assembly**: Combines all components into a complete genesis.json file with proper formatting

## Output
Generates a complete `genesis.json` file containing:
- QBFT consensus configuration with validator set encoded in extraData
- Network parameters (chain ID, gas limits, EIP activations)
- Bootnode enode URLs for peer discovery  
- Pre-deployed smart contracts with deterministically calculated addresses
- Contract allocations with maximum balance and runtime bytecode
- Proper QBFT extraData encoding with RLP structure for consensus mechanism