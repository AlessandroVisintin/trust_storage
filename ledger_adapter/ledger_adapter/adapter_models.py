from dataclasses import dataclass


@dataclass
class BlockDetails:
    block_hash: str
    block_number: str

@dataclass
class TransactionDetails:
    transaction_hash: str
    from_address: str
    to_address: str
    gas_used: str

@dataclass
class EventDetails:
    event_name: str
    event_results: list

@dataclass
class BlockchainResponse:
    status: str
    block: BlockDetails
    transaction: TransactionDetails
    event: EventDetails
