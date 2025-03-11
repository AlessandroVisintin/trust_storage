# Solidity Compiler

Docker-based utility for compiling Ethereum Solidity contracts.

## Overview

This tool automatically compiles all Solidity (`.sol`) files from the `../contracts` directory and outputs the compiled artifacts to `../build`.

## Prerequisites

- Docker
- Docker Compose

## Usage

1. Place your Solidity files in the `contracts/` directory (at the project root)
2. Run the compilation script:

```bash
cd utils/solidity_compiler
run.bat
```

3. Find compilation artifacts in the `build/` directory (at the project root)

## How It Works

The `run.bat` script:
- Loops through all `.sol` files in the `../contracts/` directory
- Sets each filename as the `CONTRACT_NAME` environment variable
- Runs Docker Compose for each file

## Outputs

For each contract, the compiler generates:
- `ContractName.abi`: Contract ABI (JSON interface)
- `ContractName.bin`: Deployable bytecode
- `ContractName.bin-runtime`: Runtime bytecode (excluding constructor)

## Example

1. Create a file `MyToken.sol` in the `contracts/` directory
2. Run `docker/run.bat`
3. Find `MyToken.abi`, `MyToken.bin`, and `MyToken.bin-runtime` in the `build/` directory
