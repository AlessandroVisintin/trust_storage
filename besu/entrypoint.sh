# #!/bin/sh

set -e

if [ -z "$NODE_NAME" ]; then
    echo "Error: NODE_NAME environment variable is not set"
    exit 1
fi
data_dir="/data/$NODE_NAME"
mkdir -p "$data_dir"


if [ -z "$BOOTNODES" ]; then
    echo "Error: BOOTNODES environment variable is not set"
    exit 1
fi
bootnodes=""
IFS=',' read -ra nodes <<< "$BOOTNODES"
for node in "${nodes[@]}"; do
    name=$(echo "$node" | cut -d'@' -f1)
    ip=$(echo "$node" | cut -d'@' -f2)
    pubkey=$(cat "/sources/nodes/$name/.pub" | sed 's/^0x//')
    enode="enode://$pubkey@$ip:$P2P_PORT"
    bootnodes="${bootnodes:+$bootnodes,}$enode"
done

ip_address=$(hostname -i | awk '{print $1}')

besu \
    --data-path=$data_dir \
    --genesis-file="/sources/genesis/genesis.json" \
    --node-private-key-file="/sources/account/.prv" \
    --min-gas-price=0 \
    --p2p-host=$ip_address \
    --p2p-port=$P2P_PORT \
    --rpc-http-enabled \
    --rpc-http-host=$ip_address \
    --rpc-http-port=$RPC_PORT \
    --rpc-http-api=ETH,NET,QBFT \
    --host-allowlist=* \
    --rpc-http-cors-origins=\"all\" \
    --bootnodes=$bootnodes \
    > "$data_dir/.log" 2>&1


find "$data_dir" -type f -name "*.jfr" -delete
