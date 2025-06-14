import ast

from hexbytes import HexBytes
from web3.contract import Contract
from web3.types import TxReceipt
from web3.exceptions import Web3RPCError

from .adapter_models import (
    BlockDetails, TransactionDetails, EventDetails,
    BlockchainResponse, BlockchainError
)


def to_0xhex(value):
    if isinstance(value, HexBytes):
        return '0x' + value.hex()
    if isinstance(value, bytes):
        return '0x' + value.hex()
    if isinstance(value, str) and not value.startswith('0x'):
        return '0x' + value
    return value

def parse_events_from_receipt(contract: Contract, receipt: TxReceipt) -> list[EventDetails]:
    parsed_events = []
    for event_abi in [abi for abi in contract.abi if abi['type'] == 'event']:
        event_name = event_abi['name']
        event_processor = getattr(contract.events, event_name)
        logs = event_processor().process_receipt(receipt)
        for log in logs:
            event_data = EventDetails(
                event_name=log.event,
                event_results=dict(log.args)
            )
        parsed_events.append(event_data)
    return parsed_events

def parse_response_from_receipt(contract: Contract, receipt: TxReceipt) -> BlockchainResponse:        
    return BlockchainResponse(
        status=str(receipt.status),
        block=BlockDetails(
            block_hash=to_0xhex(receipt.blockHash),
            block_number=str(receipt.blockNumber)
        ),
        transaction=TransactionDetails(
            transaction_hash=to_0xhex(receipt.transactionHash),
            from_address=str(receipt['from']),
            to_address=str(receipt['to']),
            gas_used=str(receipt.gasUsed)
        ),
        events=parse_events_from_receipt(contract, receipt)
    )

def parse_error(error: Web3RPCError) -> BlockchainError:
    if isinstance(error, Web3RPCError):    
        try:
            error_details_str = error.args[0]
            error_dict = ast.literal_eval(error_details_str)
            message = error_dict.get('message', str(error))
            return BlockchainError(message=message, status=0)

        except (ValueError, SyntaxError, IndexError):
            return BlockchainError(message=str(error), status=0)

    return BlockchainError(message=str(error), status=0)