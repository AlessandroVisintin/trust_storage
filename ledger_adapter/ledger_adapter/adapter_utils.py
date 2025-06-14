from hexbytes import HexBytes

from .adapter_models import BlockDetails, TransactionDetails, EventDetails, BlockchainResponse


def to_0xhex(value):
    if isinstance(value, HexBytes):
        return '0x' + value.hex()
    if isinstance(value, bytes):
        return '0x' + value.hex()
    if isinstance(value, str) and not value.startswith('0x'):
        return '0x' + value
    return value

def parse_blockchain_response(data: dict) -> BlockchainResponse:
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
