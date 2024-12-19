# QBFT Genesis Creator

This Docker application generates a `genesis.json` file for a Besu QBFT (Quorum Byzantine Fault Tolerance) network based on provided inputs.

## Inputs and Outputs

### Inputs

The application requires the following inputs:

1. **Validator Information**
   - Environment Variable: `VALIDATORS` (comma-separated list of validator names)
   - Required Files: `.address` for each validator
   - Content: Ethereum address of the validator

2. **Bootnode Information**
   - Environment Variable: `BOOTNODES` (comma-separated list of bootnode names)
   - Required Files: `.pub` for each bootnode
   - Content: Public key of the bootnode

3. **Contract Information**
   - Environment Variable: `CONTRACTS` (comma-separated list of contract names)
   - Required Files: `.bin-runtime` for each contract
   - Content: Runtime bytecode of the contract

### Outputs

The application generates the following outputs in the `./output` directory:

1. `genesis.json`: The main genesis file for the Besu QBFT network, which includes:
   - A custom `bootnodes` field containing a list of enode URLs for available bootnodes. Each enode URL follows the format `"enode://..pubkey..@{node name}"`, where `{node name}` serves as a placeholder for the future IP:PORT of the node.
   - An `alloc` field that pre-deploys the specified contracts with their bytecode and initial balance.

2. `{contract_name}.address`: A file for each contract containing its calculated address

## Usage

1. Prepare the input files as described above.
2. Modify the `docker-compose.yml` file to map the files into the correct volumes:

```yaml
volumes:
  - /path/to/node/.pub:/nodes/node/.pub
  - ...
  - /path/to/contract/contract.bin-runtime:/contracts/contract/contract.bin-runtime
  - ...
```

3. Set the required environment variables in the `docker-compose.yml` file:

```yaml
environment:
  BOOTNODES: node0,node1
  VALIDATORS: validator0,validator1
  CONTRACTS: contract0,contract1
```

4. Run the application:

```sh
docker-compose up
```

5. Retrieve the generated `genesis.json` and contract address files from the output directory.
