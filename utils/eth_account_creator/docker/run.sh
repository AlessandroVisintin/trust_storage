#!/bin/bash

cd "$(dirname "$0")"

mkdir -p "../build" 2>/dev/null

docker compose build

read -p "How many Ethereum accounts do you want to create? " NUM_ACCOUNTS

for ((i=1; i<=NUM_ACCOUNTS; i++)); do
    echo "Creating account $i of $NUM_ACCOUNTS..."
    docker compose run --rm eth_account_generator
done
