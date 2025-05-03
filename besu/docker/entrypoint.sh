# #!/bin/sh

# required
data_dir="/sources/account/data/"
prvkey_file="/sources/account/.prv"
genesis_file="/sources/network/genesis.json"
boot_file="/sources/network/bootnodes.txt"
# optional
perm_file="/sources/network/permissions.toml"


if [ ! -f "$genesis_file" ]; then
    echo "Error: Genesis file does not exist at $genesis_file" >&2
    exit 1
fi

if [ ! -f "$prvkey_file" ]; then
    echo "Error: Private key file does not exist at $prvkey_file" >&2
    exit 1
fi

if [ ! -d "$data_dir" ]; then 
    mkdir -p "$data_dir"
fi

bootnodes_param=""
if [ -f "$boot_file" ]; then
    bootnodes_list=$(tr '\n' ',' < "$boot_file" | sed 's/,$//')
    if [ -n "$bootnodes_list" ]; then
        bootnodes_param="--bootnodes=$bootnodes_list"
    else
        echo "Error: Empty bootnodes list at $boot_file" >&2
        exit 1
    fi
else
    echo "Error: Bootnodes file does not exist at $boot_file" >&2
    exit 1
fi

permissions_param=""
if [ -f $perm_file ]; then
    permissions_param="--permissions-accounts-config-file-enabled=true"
    permissions_param+=" --permissions-accounts-config-file=$perm_file"
fi

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
    --rpc-http-api=ETH,NET,QBFT \
    --host-allowlist=* \
    $bootnodes_param \
    $permissions_param \
    > "$data_dir/.log" 2>&1

# Delete .jfr files
find "$data_dir" -type f -name "*.jfr" -delete