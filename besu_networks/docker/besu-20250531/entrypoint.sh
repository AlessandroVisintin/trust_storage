#!/bin/sh

#
# Hyperledger Besu Docker Container Entrypoint
#
# This script serves as the entrypoint for a Besu Docker image, exposing the blockchain node
# on ports 8545 (RPC) and 30303 (P2P) for external communication.
#
# The image is designed for flexibility through standardized file paths that can be easily
# configured via Docker volume bindings:
# - Mount custom genesis.json, private.key, bootnodes.txt, and permissions files to override defaults
# - Bind the /sources/data directory to persist blockchain state across container restarts
# - Reuse the same image for different network configurations without rebuilding
#
# Volume binding the data directory makes the container stateful, preserving blockchain
# data, logs, and node state between container lifecycle operations.
#

# Main data directory where blockchain data, logs, and runtime files are stored
data_dir="/sources/data"

# Private key file for the node's identity and transaction signing
prvkey_file="/sources/account/private.key"

# Genesis block configuration defining the initial blockchain state
genesis_file="/sources/network/genesis.json"

# List of initial peer nodes to connect to for network discovery
bootnodes_file="/sources/network/bootnodes.txt"

# Optional permissions configuration for network access control
perm_file="/sources/network/permissions_config.toml"

##

# Validate that the genesis file exists (required for blockchain initialization)
if [ ! -f "$genesis_file" ]; then
    echo "Genesis file does not exist at $genesis_file" >&2
    exit 1
fi
echo "$genesis_file found"

# Validate that the private key file exists (required for node identity)
if [ ! -f "$prvkey_file" ]; then
    echo "Private key file does not exist at $prvkey_file" >&2
    exit 1
fi
echo "$prvkey_file found"

# Create data directory if it doesn't exist (for storing blockchain data and logs)
if [ ! -d "$data_dir" ]; then 
    mkdir -p "$data_dir"
    echo "$data_dir created"
fi

# Validate and process the bootnodes file (required for peer discovery)
if [ ! -f "$bootnodes_file" ]; then
    echo "Bootnodes file does not exist at $bootnodes_file" >&2
    exit 1
fi
# Parse bootnodes file: remove empty lines, trim whitespace, join with commas
echo "Reading bootnodes from $bootnodes_file"
bootnodes_list=$(grep -v '^[[:space:]]*$' "$bootnodes_file" 2>/dev/null | \
                 sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | \
                 tr '\n' ',' | \
                 sed 's/,$//')

if [ -z "$bootnodes_list" ]; then
    echo "Error: Empty bootnodes list in $bootnodes_file" >&2
    exit 1
fi
bootnodes_param="--bootnodes=$bootnodes_list"
echo "Bootnodes parsed"

# Handle optional permissions configuration
permissions_param=""
# Base RPC APIs (Ethereum, Network, QBFT consensus)
rpc_http_api_param="--rpc-http-api=ETH,NET,QBFT"
# If permissions file exists, copy it to data directory and enable permissions API
if [ -f "$perm_file" ]; then
    cp "$perm_file" "$data_dir/"
    rpc_http_api_param="${rpc_http_api_param},PERM"
    permissions_param="--permissions-accounts-config-file-enabled=true"
    echo "$perm_file copied to $data_dir"
fi

# Start the Hyperledger Besu blockchain node
echo "Starting node.."
besu \
    --data-path=$data_dir \
    --genesis-file=$genesis_file \
    --node-private-key-file=$prvkey_file \
    --min-gas-price=0 \
    --p2p-enabled=true \
    --p2p-host=0.0.0.0 \
    --p2p-port=30303 \
    --rpc-http-enabled=true \
    --rpc-http-host=0.0.0.0 \
    --rpc-http-port=8545 \
    --rpc-http-cors-origins="all" \
    $rpc_http_api_param \
    --host-allowlist=* \
    $bootnodes_param \
    $permissions_param \
    > "$data_dir/.log" 2>&1

# Clean up Java Flight Recorder files (performance profiling files that can accumulate)
find "$data_dir" -type f -name "*.jfr" -delete