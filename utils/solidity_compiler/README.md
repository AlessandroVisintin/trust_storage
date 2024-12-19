# Solidity Compiler Docker App

This Docker application provides a convenient way to compile Solidity smart contracts using the official Ethereum Solidity compiler (solc) in a containerized environment.

## Overview

The app uses the `ethereum/solc:stable` image to compile Solidity contracts. It mounts local directories for input and output, allowing you to easily manage your source files and compilation results.

## Configuration

The `docker-compose.yml` file defines a single service named `solc`:

```yaml
services:
    solc:
        image: ethereum/solc:stable
        volumes:
            - ./data:/sources
            - ./.output/:/output
        command: "--output-dir /output --overwrite --abi --bin --bin-runtime /sources/HashManager.sol"
```


## Inputs and Outputs

### Inputs

- **Source Files**: Place your Solidity source files in the `./data` directory on your host machine. This directory is mounted to `/sources` inside the container.
- **Target File**: Set the command in the docker-compose file to compile the specific file (example: `/sources/HashManager.sol`).

### Outputs

The compiler generates output files in the `./.output/`. The following output files are generated:

- **ABI (Application Binary Interface)**: JSON file describing the contract's interface.
- **Binary**: Raw compiled bytecode of the contract.
- **Binary Runtime**: Runtime bytecode of the contract, which excludes the constructor and initialization code.

## Compiler Options

The command uses several options to control the compilation process:

- `--output-dir /output`: Specifies the output directory for compiled files.
- `--overwrite`: Allows overwriting existing files in the output directory.
- `--abi`: Generates the ABI (Application Binary Interface) file.
- `--bin`: Generates the binary (bytecode) file.
- `--bin-runtime`: Generates the runtime binary file.

## Usage

1. Place your Solidity source files in the `./data` directory.
2. Run the Docker container using `docker-compose up`.
4. Check the `./.output/` directory for the compiled files.
