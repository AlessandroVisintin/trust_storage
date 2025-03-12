# Besu QBFT Genesis Creator  
**Docker-based utility for generating Hyperledger Besu QBFT genesis files.**  

## Overview  
This tool automates creation of QBFT consensus genesis files for Besu blockchains. It processes:  
- **Validator addresses**  
- **Bootnode connections**  
- **Precompiled contracts**  

Generates a complete `genesis.json` file with:  
- Validator set in `extraData`  
- Network bootnodes  
- Contract allocations with balances  

## Prerequisites  
- Docker  
- Docker Compose  

## Usage  
1. Prepare input files:  
   - `bootnodes.txt`: Enode entries (format: `0xpubkey@address`)  
   - `validators.txt`: Ethereum addresses (one per line)  
   - `contracts/`: Directory with contract bytecode files (`*.bin-runtime`)  

2. Run generator:  
```bash 
.\docker\run.bat 
```

3. Find `genesis.json` in `build/` directory  

## File Structure  
```bash
data/
├── bootnodes.txt       # Network bootstrap nodes
├── validators.txt      # Validator addresses  
└── contracts/          # Contract bytecode files (*.bin-runtime)
build/
└── genesis.json        # Generated configuration
```

## How It Works  
1. **Input Processing**  
   - Validators: Generates QBFT `extraData` header  
   - Bootnodes: Creates enode URLs list  
   - Contracts: Allocates addresses with balances  

2. **Address Generation**  
Contracts receive deterministic addresses using:  
`keccak("Rescale{{contractName}}")[0..20]`  

3. **Docker Pipeline**  
- Builds Rust executable in container  
- Maps directories:  
  - `/sources`: Input files  
  - `/output`: Generated genesis.json  

## Input File Formats  
**bootnodes.txt**  
```text
0x{{pubkey1}}@{{nodeAddress | placeholder}}
0x{{pubkey}}@{{nodeAddress | placeholder}}
```

**validators.txt**  
```text
0xBf0dFc0132D3D0Aaf652D42aAbC2D391862478Dc
0x2D319DdF7F962B9ca8E70E2F2B9070bCA087c8d5
```

**contracts/**  
```bash
MyContract.bin-runtime  # Runtime bytecode
```

## Output  
`genesis.json` contains:  
- QBFT consensus parameters  
- Pre-configured validators  
- Network bootnodes  
- Contract allocations with:  
  - Max ETH balance (`0xff...ff`)  
  - Provided bytecode  
  - Empty storage  

## Example  
1. Add validator addresses to `validators.txt`
1. Add bootnodes addresses to `validators.txt`  
2. Place contract bytecode in `contracts/`  
3. Execute `docker/run.bat`  
4. Use generated `build/genesis.json` for network initialization  

```json
{
  "config": {
    "qbft": {
      "blockperiodseconds": 5,
      "epochlength": 30000
    }
  },
  "extraData": "0x...040ec65...",
  "bootnodes": [
    "enode://a5...@placeholder"
  ],
  "alloc": {
    "0xb6...": {
      "code": "0x608...06003",
      "balance": "0xffff...ffff"
    }
  }
}