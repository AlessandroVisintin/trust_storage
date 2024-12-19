FROM hyperledger/besu:24.9.1

COPY ./utils/besu_qbft_genesis_creator/.output/genesis.json /sources/genesis.json
COPY ./besu/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]