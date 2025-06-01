import json
import rlp
from pathlib import Path
from typing import Any, Dict, List, Optional


class AllocationItem:
    def __init__(
        self,
        address: str,
        balance: str,
        code: Optional[str] = None,
        storage: Optional[Dict[str, str]] = None,
    ):
        self._address = address
        self._balance = balance
        self._code = code
        self._storage = storage or {}

    def get_address(self) -> str:
        return self._address

    def get_balance(self) -> str:
        return self._balance

    def get_code(self) -> Optional[str]:
        return self._code

    def get_storage(self) -> Dict[str, str]:
        return self._storage

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"balance": self._balance}
        if self._code is not None:
            data["code"] = self._code
        if self._storage:
            data["storage"] = self._storage
        return data


class AllocationManager:
    def __init__(self, items: Optional[List[AllocationItem]] = None):
        self._items = items or []

    def add_item(self, item: AllocationItem) -> None:
        self._items.append(item)

    def to_dict(self) -> Dict[str, Any]:
        alloc: Dict[str, Any] = {}
        for item in self._items:
            alloc[item.get_address()] = item.to_dict()
        return alloc


class HardForkItem:
    def __init__(self, name: str, block_number: int):
        self.name = name
        self.block_number = block_number

    def to_dict(self) -> Dict[str, int]:
        return {self.name: self.block_number}


class HardForkManager:
    def __init__(self, forks: Optional[List[HardForkItem]] = None):
        self._forks = forks or []

    def add_fork(self, fork: HardForkItem) -> None:
        self._forks.append(fork)

    def to_dict(self) -> Dict[str, int]:
        cfg: Dict[str, int] = {}
        for fork in self._forks:
            cfg.update(fork.to_dict())
        return cfg


class ConsensusItem:
    def get_config(self) -> Dict[str, Any]:
        raise NotImplementedError

    def get_extradata(self) -> str:
        raise NotImplementedError


class QbftConsensusItem(ConsensusItem):
    def __init__(self,
                 validators: List[str],
                 block_period_seconds: int,
                 epoch: int,
                 request_timeout_seconds: int):
        self.validators = validators
        self.block_period_seconds = block_period_seconds
        self.epoch = epoch
        self.request_timeout_seconds = request_timeout_seconds

    def get_config(self) -> Dict[str, Any]:
        return {
            "qbft": {
                "blockperiodseconds": self.block_period_seconds,
                "epochlength": self.epoch,
                "requesttimeoutseconds": self.request_timeout_seconds
            }
        }

    def get_extradata(self) -> str:
        vanity = b'\x00' * 32 
        decoded = [bytes.fromhex( v.strip("0x") ) for v in self.validators]
        vote = []
        round_number = 0
        seals = []
        payload = [vanity, decoded, vote, round_number, seals]
        return f"0x{ rlp.encode(payload).hex() }"


class ConfigManager:
    def __init__(
        self,
        hard_forks: HardForkManager,
        consensus: ConsensusItem,
        chain_id: int,
        contract_size_limit: int,
        zero_base_fee: bool
    ):
        self.hard_forks = hard_forks
        self.consensus = consensus
        self.chain_id = chain_id
        self.contract_size_limit = contract_size_limit
        self.zero_base_fee = zero_base_fee

    def to_dict(self) -> Dict[str, Any]:
        cfg = {
            "chainId": self.chain_id,
            "contractSizeLimit": self.contract_size_limit,
            "zeroBaseFee": self.zero_base_fee
            }
        cfg.update(self.hard_forks.to_dict())
        cfg.update(self.consensus.get_config())
        return cfg


class GenesisManager:
    def __init__(
        self,
        difficulty: str,
        gas_limit: str,
        mix_hash: str,
        nonce: str,
        timestamp: str,
        coinbase: str,
        alloc_manager: AllocationManager,
        config_manager: ConfigManager,
    ):
        self.difficulty = difficulty
        self.gasLimit = gas_limit
        self.mixHash = mix_hash
        self.nonce = nonce
        self.timestamp = timestamp
        self.coinbase = coinbase
        self.alloc_manager = alloc_manager
        self.config_manager = config_manager
        self.extraData = config_manager.consensus.get_extradata()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "config": self.config_manager.to_dict(),
            "alloc": self.alloc_manager.to_dict(),
            "difficulty": self.difficulty,
            "gasLimit": self.gasLimit,
            "mixHash": self.mixHash,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "coinbase": self.coinbase,
            "extraData": self.extraData,
        }

    def save_to_file(self, filepath: str) -> None:
        path = Path(filepath)
        path.write_text(json.dumps(self.to_dict(), indent=2))
