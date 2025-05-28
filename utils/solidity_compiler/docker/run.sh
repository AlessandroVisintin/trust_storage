#!/bin/bash

folder="$(cd "$(dirname "$0")" && pwd)"
if [ ! -f "$folder/docker-compose.yaml" ]; then
    echo "Error: docker-compose.yaml not found in script directory."
    exit 1
fi

mkdir -p "$folder/../build"

echo "Searching for .sol files in $folder"
echo

for file in "$folder"/../contracts/*.sol; do

    if [ ! -f "$file" ]; then
        continue
    fi
    
    filename=$(basename "$file" .sol)
    
    echo "Processing contract: $filename.sol"
    echo
    
    CONTRACT_NAME="$filename" docker compose -f "$folder/docker-compose.yaml" up
    
    echo
    if [ $? -eq 0 ]; then
        echo "Successfully processed $filename.sol"
    else
        echo "Error: Docker Compose failed for $filename.sol"
    fi
    echo
done

echo
echo "Search completed."
