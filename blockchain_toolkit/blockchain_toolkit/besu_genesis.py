from typing import Optional,Dict,List,Any
from dataclasses import dataclass, asdict

from .eth_utils import snake_case_to_camel_case
from .besu_consensus import ConsensusConfig


@dataclass
class GenesisAllocation:
    balance: str
    code: Optional[str] = ""
    storage: Optional[Dict[str, str]] = None

    def __post_init__(self):
        if self.storage is None:
            self.storage = {}

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        if not result['storage']:
            del result['storage']
        if not result['code']:
            del result['code']
        return result


@dataclass
class GenesisHardFork:
    name: str
    block_number: int = 0

    def to_dict(self) -> Dict[str, int]:
        return {snake_case_to_camel_case(self.name): self.block_number}


@dataclass
class GenesisConfig:
    chain_id: int
    hard_forks: List[GenesisHardFork]
    contract_size_limit: int = 2147483647
    zero_base_fee: bool = True
    consensus_config: Optional[ConsensusConfig] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "chainId": self.chain_id,
            "contractSizeLimit": self.contract_size_limit,
            "zeroBaseFee": self.zero_base_fee,
        }
        for hard_fork in self.hard_forks:
            result.update(hard_fork.to_dict())
        if self.consensus_config:
            result[self.consensus_config.consensus_name()] = self.consensus_config.to_dict()
        return result


@dataclass
class GenesisBlock:
    config: GenesisConfig
    alloc: List[GenesisAllocation] = []
    coinbase: str = "0x0000000000000000000000000000000000000000"
    difficulty: str = "0"
    gas_limit: str = "0x1fffffffffffff"
    nonce: str = "0x0000000000000000"
    mix_hash: str = "0x0000000000000000000000000000000000000000000000000000000000000000"
    parent_hash: str = "0x0000000000000000000000000000000000000000000000000000000000000000"
    timestamp: str = "0x0"
    extra_data: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        # Serialize allocations
        alloc_dict = {
            address: allocation.to_dict() 
            for address, allocation in self.alloc.items()
        }
        return {
            "config": self.config.to_dict(),
            "alloc": alloc_dict,
            "coinbase": self.coinbase,
            "difficulty": self.difficulty,
            "gasLimit": snake_case_to_camel_case("gas_limit"),
            "nonce": self.nonce,
            "mixHash": snake_case_to_camel_case("mix_hash"),
            "parentHash": snake_case_to_camel_case("parent_hash"),
            "timestamp": self.timestamp,
            "extraData": snake_case_to_camel_case("extra_data")
        }
