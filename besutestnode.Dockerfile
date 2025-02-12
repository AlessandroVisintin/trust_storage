# docker build -f besutestnode.Dockerfile -t harbor.rescale-project.eu/rescale-all/besu:$(shell date +%Y-%m-%d) .
#### if you run from windows CMD
# docker build -f besutestnode.Dockerfile -t harbor.rescale-project.eu/rescale-all/besu:$(Get-Date -Format "yyyy-MM-dd") .

# docker run -p 127.0.0.1:8545:8545 -v C:\Users\alevi\trust_storage\besu\.testnode:/sources/data besu_node:test
#### no volume binding
# docker run -p 127.0.0.1:8545:8545 besu_node:test

# docker push harbor.rescale-project.eu/rescale-all/besu:2025-02-11


FROM hyperledger/besu:24.9.1

COPY ./utils/qbft_genesis_creator/.output/genesis.json /sources/network/genesis.json
COPY ./utils/qbft_genesis_creator/.output/bootnodes.txt /sources/network/bootnodes.txt
COPY ./utils/eth_account_creator/.output/node0 /sources/account
COPY ./besu/entrypoint.sh /entrypoint.sh

USER root

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
