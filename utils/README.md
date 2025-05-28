# Ethereum Development Utils

A collection of Docker-based utilities for Ethereum blockchain development and network setup.

## Overview

This directory contains three essential tools for Ethereum development workflows, each containerized with Docker for easy deployment and cross-platform compatibility. These utilities cover the complete lifecycle from account creation to smart contract compilation and network genesis generation.

## Tools

### **eth_account_creator**
Generates cryptographically secure Ethereum wallet accounts with private keys, public keys, and addresses. Uses secp256k1 elliptic curve cryptography and Keccak-256 hashing to create accounts compatible with all Ethereum-based applications.

### **qbft_genesis_creator** 
Creates production-ready genesis.json files for Ethereum networks using QBFT (Istanbul BFT 2.0) consensus mechanism. Processes validator addresses, bootnode configurations, and smart contract bytecode to generate complete network initialization files.

### **solidity_compiler**
Compiles Ethereum Solidity smart contracts and outputs compiled artifacts including ABI, deployable bytecode, and runtime bytecode. Automatically processes all `.sol` files from the contracts directory.

## Prerequisites

- Docker
- Docker Compose

## Usage

Each tool is self-contained with its own configuration and execution scripts. Navigate to the specific tool directory and refer to its individual README.md for detailed usage instructions, configuration options, and examples.

**Quick start for each tool:**
- **Windows**: Run `docker/run.bat` 
- **Linux/Mac**: Run `docker/run.sh` (with appropriate parameters)

## Workflow Integration

These tools are designed to work together in a typical Ethereum development workflow:

1. **eth_account_creator**: Generate validator and bootnode accounts
2. **solidity_compiler**: Compile smart contracts for deployment
3. **qbft_genesis_creator**: Create network genesis file using accounts and contracts

Each tool outputs to a `build/` directory within its respective folder for easy integration with subsequent steps.