#!/bin/bash

#SCRIPT_DIR="$(dirname "$0")"
#mkdir -p "$SCRIPT_DIR/../build"

# for sol_file in $SCRIPT_DIR/contracts/*.sol; do
#     if [ ! -f "$sol_file" ]; then
#         echo "No .sol files found in ../contracts/"
#         exit 1
#     fi
    
#     filename=$(basename "$sol_file")
#     echo "Compiling $filename..."
    
#     CONTRACT_NAME="$filename" docker compose run --rm solc
    
#     if [ $? -eq 0 ]; then
#         echo "Successfully compiled $filename"
#     else
#         echo "Error compiling $filename"
#     fi

# done