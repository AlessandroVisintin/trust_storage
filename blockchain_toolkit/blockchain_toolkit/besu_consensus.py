from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Dict, Any

from .eth_utils import snake_case_to_camel_case


class ConsensusConfig(ABC):
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass
    
    @property
    @abstractmethod
    def consensus_name(self) -> str:
        pass


@dataclass
class QBFTConsensusConfig(ConsensusConfig):
    block_period_seconds: int = 5
    epoch_length: int = 30000
    request_timeout_seconds: int = 10
    round_change_timer_seconds: int = 10
    message_queue_size_limit: int = 1000
    duplicate_message_limit: int = 100
    future_msgs_size_limit: int = 1000
    future_msgs_max_distance: int = 10
    
    @property
    def consensus_name(self) -> str:
        return "qbft"
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return {
            snake_case_to_camel_case(key): value 
            for key, value in data.items()
        }