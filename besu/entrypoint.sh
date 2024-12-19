# #!/bin/sh

set -e

hostname=$(hostname)
data_dir="/opt/besu/${hostname}"
mkdir -p "$data_dir"

sleep infinity

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
    --p2p-port-enabled \
    --p2p-host=127.0.0.1 \
    --p2p-port=8545 \
    --rpc-http-enabled \
    --rpc-http-host=127.0.0.1 \
    --rpc-http-port=30303 \
    --rpc-http-cors-origins=\"all\" \
    --rpc-http-api=ETH,NET,QBFT \
    --host-allowlist=* \
    --bootnodes=$bootnodes \
    > "$data_dir/.log" 2>&1


find "$data_dir" -type f -name "*.jfr" -delete
