FROM rust:latest AS builder
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y libssl-dev pkg-config
RUN cargo new --bin eth_account_creator
WORKDIR /usr/src/app/eth_account_creator
RUN cargo add secp256k1@0.27.0 && \
    cargo add rand@0.8.5 && \
    cargo add hex@0.4.3 && \
    cargo add serde_json@1.0.96 && \
    cargo add sha3@0.10.8
COPY ./main.rs src/main.rs
RUN cargo build --release

FROM gcr.io/distroless/cc
WORKDIR /src
COPY --from=builder /usr/src/app/eth_account_creator/target/release/eth_account_creator ./
CMD ["/src/eth_account_creator"]