# docker build -f clienttestnode.Dockerfile -t client_node:test .
# docker run --network host client_node:test

FROM python:3.12-alpine

COPY ./trust_storage_client /sources/trust_storage_client
COPY ./trust_storage_client/tests/data/keys /sources/account
COPY ./trust_storage_client/tests/data/contracts /sources/contracts

ENV BESU_ENDPOINT=http://127.0.0.1:8545
ENV CONTRACT_ADDR_PATH=/sources/contracts/HashManager.address
ENV CONTRACT_JSON_PATH=/sources/contracts/HashManager.abi
ENV CLIENT_PRVKEY_PATH=/sources/account/.prv
ENV CLIENT_PUBKEY_PATH=/sources/account/.pub

RUN apk add --no-cache --virtual .build-deps musl-dev curl \
    && pip install -e /sources/trust_storage_client \
    && pip install --no-cache-dir -r /sources/trust_storage_client/requirements.txt \
    && apk del .build-deps

CMD ["python", "/sources/trust_storage_client/tests/keepalive.py"]
