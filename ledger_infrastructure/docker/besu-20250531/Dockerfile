FROM hyperledger/besu:24.9.1

USER root

COPY ./docker/besu-20250531/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]