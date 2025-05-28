#!/bin/bash

set -e

read_config_file() {
    local config_file="$1"
    if [[ ! -f "$config_file" ]]; then
        echo "Error: Configuration file '$config_file' not found"
        exit 1
    fi
    
    echo "Reading configuration from: $config_file"
    
    while IFS='=' read -r key value; do
        # Skip empty lines and comments
        [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue        
        # Remove leading/trailing whitespace
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        case "$key" in
            contracts)
                contracts="$value"
                ;;
            bootnodes)
                bootnodes="$value"
                ;;
            validators)
                validators="$value"
                ;;
        esac
    done < "$config_file"
}

cd "$(dirname "$0")"

mkdir -p ../data
mkdir -p ../data/contracts

contracts=""
bootnodes=""
validators=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            read_config_file "$2"
            shift 2
            ;;
        --contracts)
            contracts="$2"
            shift 2
            ;;
        --bootnodes)
            bootnodes="$2"
            shift 2
            ;;
        --validators)
            validators="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 --contracts 'path1,path2' --bootnodes 'node1,node2' --validators 'val1,val2'"
            echo ""
            echo "Options:"
            echo "  --contracts   Comma-separated list of contract paths (reads .bin-runtime files)"
            echo "  --bootnodes   Comma-separated list of node paths (reads .address files)"
            echo "  --validators  Comma-separated list of node paths (reads .pubkey files)"
            echo "  -h, --help    Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown parameter: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Handle contracts parameter
if [[ -n "$contracts" ]]; then
    echo "Processing contracts..."
    IFS=',' read -ra CONTRACT_ARRAY <<< "$contracts"
    for contract_path in "${CONTRACT_ARRAY[@]}"; do
        # Remove leading/trailing whitespace
        contract_path=$(echo "$contract_path" | xargs)
        runtime_file="$contract_path.bin-runtime"
        if [[ -f "$runtime_file" ]]; then
            echo "  Copying: $runtime_file"
            cp "$runtime_file" ../data/contracts/
        else
            echo "  Warning: Contract file not found: $runtime_file"
        fi
    done
fi

# Handle bootnodes parameter (store .address content in validators.txt)
if [[ -n "$bootnodes" ]]; then
    echo "Processing bootnodes..."
    > ../data/validators.txt  # Clear the file
    IFS=',' read -ra BOOTNODE_ARRAY <<< "$bootnodes"
    for node_path in "${BOOTNODE_ARRAY[@]}"; do
        # Remove leading/trailing whitespace
        node_path=$(echo "$node_path" | xargs)
        address_file="$node_path/.address"
        if [[ -f "$address_file" ]]; then
            echo "  Reading address from: $address_file"
            cat "$address_file" >> ../data/validators.txt
        else
            echo "  Warning: Address file not found: $address_file"
        fi
    done
fi

# Handle validators parameter
if [[ -n "$validators" ]]; then
    echo "Processing validators..."
    > ../data/bootnodes.txt  # Clear the file
    IFS=',' read -ra VALIDATOR_ARRAY <<< "$validators"
    for node_path in "${VALIDATOR_ARRAY[@]}"; do
        # Remove leading/trailing whitespace
        node_path=$(echo "$node_path" | xargs)
        pubkey_file="$node_path/.pub"
        if [[ -f "$pubkey_file" ]]; then
            echo "  Reading pubkey from: $pubkey_file"
            pubkey_content=$(cat "$pubkey_file")
            echo "${pubkey_content}@placeholder" >> ../data/bootnodes.txt
        else
            echo "  Warning: Pubkey file not found: $pubkey_file"
        fi
    done
fi

mkdir -p "$folder/../build"

docker compose build

docker compose run --rm qbft_genesis_creator

echo "Script completed successfully!"