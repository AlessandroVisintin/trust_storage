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
    events: list[EventDetails]

    @classmethod
    def from_blockchain_response(cls, data: dict) -> 'BlockchainResponse':
        return BlockchainResponse(
            status = str(data['status']),
            block =  BlockDetails(
                block_hash = to_0xhex(data['blockHash']),
                block_number = data['blockNumber']
            ),
            transaction = TransactionDetails(
                transaction_hash = to_0xhex(data['transactionHash']),
                from_address = data['from'],
                to_address = data['to'],
                gas_used = data['gasUsed']
            ),
            event_details = None
        )

@dataclass
class BlockchainError:
    message: str
    status: int=0
