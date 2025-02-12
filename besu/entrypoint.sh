# #!/bin/sh

set -e

bootnodes=""
echo "Initial bootnodes: $bootnodes"

if [ -n "$BOOTNODES" ]; then
    echo "BOOTNODES environment variable is set"
    echo "BOOTNODES content: $BOOTNODES"

    # Read BESU_BOOTNODES into an associative array
    eval "$(echo "$BOOTNODES" | sed 's/,/\n/g' | sed 's/\(.*\)@\(.*\)/node_\1=\2/')"
    echo "Associative array created from BOOTNODES"

    while IFS= read -r line; do
        echo "Processing line: $line"
        node_name=$(echo "$line" | sed -n 's/^enode:\/\/[^@]*@\([^:]*\).*/\1/p')
        echo "Extracted node_name: $node_name"

        # Get the corresponding IP using indirect variable reference
        ip_var="node_$node_name"
        ip=$(eval echo \$$ip_var)
        echo "IP for $node_name: $ip"

        if [ -n "$ip" ]; then
            echo "IP found for $node_name, updating bootnode"
            new_line=$(echo "$line" | sed "s/@$node_name/@$ip/")
            echo "Updated line: $new_line"
            bootnodes="${bootnodes:+$bootnodes,}$new_line"
            echo "Current bootnodes: $bootnodes"
        else
            echo "No IP found for $node_name, skipping"
        fi
    done < "/sources/network/bootnodes.txt"
    echo "Finished processing /sources/network/bootnodes.txt"
else
    echo "BOOTNODES environment variable is not set"
fi

echo "Final bootnodes: $bootnodes"

data_dir=/sources/data
if [ ! -d "$data_dir" ]; then mkdir -p "$data_dir"; fi

besu \
    --data-path=$data_dir \
    --genesis-file="/sources/network/genesis.json" \
    --node-private-key-file="/sources/account/.prv" \
    --min-gas-price=0 \
    --p2p-enabled=true \
    --p2p-host=0.0.0.0 \
    --p2p-port=30303 \
    --rpc-http-enabled=true \
    --rpc-http-host=0.0.0.0 \
    --rpc-http-port=8545 \
    --rpc-http-cors-origins=\"all\" \
    --rpc-http-api=ETH,NET,QBFT \
    --host-allowlist=* \
    --bootnodes=$bootnodes \
    > "$data_dir/.log" 2>&1


find "$data_dir" -type f -name "*.jfr" -delete
