#!/bin/sh

ipfs bootstrap rm all
if [ -n "$BOOTSTRAPS" ]; then
    old_IFS=$IFS
    IFS=','
    for node in "$BOOTSTRAPS"; do
        IFS=$old_IFS
        name=$(printf '%s' "$node" | cut -d'@' -f1)
        ip=$(printf '%s' "$node" | cut -d'@' -f2)
        peerid=$(cat "/network/$name/peer.id")
        ipfs bootstrap add "/ip4/$ip/tcp/$P2P_PORT/ipfs/$peerid"
    done
    IFS=$old_IFS
fi

peerid=$(ipfs id | sed -n 's/.*"ID": "\([^"]*\)".*/\1/p')
echo "$peerid" > "$IPFS_PATH/peer.id"
