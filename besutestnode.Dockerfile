# docker build -f besutestnode.Dockerfile -t besu_node:test .
# docker run -p 127.0.0.1:8545:8545 -v C:\Users\alevi\trust_storage\besu\.testnode:/sources/data besu_node:test

FROM hyperledger/besu:24.9.1

COPY ./utils/qbft_genesis_creator/.output/genesis.json /sources/network/genesis.json
COPY ./utils/qbft_genesis_creator/.output/bootnodes.txt /sources/network/bootnodes.txt
COPY ./utils/eth_account_creator/.output/node0 /sources/account
COPY ./besu/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
