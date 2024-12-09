# Use the official Rust image as the base
FROM rust:latest AS builder

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y libssl-dev pkg-config
RUN cargo new --bin besu_qbft_genesis_creator

WORKDIR /usr/src/app/besu_qbft_genesis_creator

RUN cargo add hex@0.4.3 && \
    cargo add rlp@0.5.2 && \
    cargo add serde_json@1.0 && \
    cargo add ethaddr@0.2.2

COPY ./main.rs src/main.rs

RUN cargo build --release


FROM gcr.io/distroless/cc

WORKDIR /src

COPY --from=builder /usr/src/app/besu_qbft_genesis_creator/target/release/besu_qbft_genesis_creator ./

CMD ["/src/besu_qbft_genesis_creator"]