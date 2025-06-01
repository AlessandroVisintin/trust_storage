from typing import List

from .besu_genesis import (
    AllocationManager, AllocationItem,
    HardForkManager, HardForkItem,
    QbftConsensusItem, ConfigManager,
    GenesisManager
    )
from .smart_contract import SmartContract
from .eth_account import EthAccount
from .eth_utils import to_checksum_address


class RescaleFreenetGenesis:

    @staticmethod
    def contract_address(contract: SmartContract):
        address_string = f"Rescale{contract.name}"
        address_hex = address_string.encode().hex()
        if len(address_hex) >= 40:
            return to_checksum_address(f"0x{address_hex[:40]}")
        return to_checksum_address(f"0x{address_hex.ljust(40, '0')}")

    def __init__(
            self,
            contracts: List[SmartContract],
            validators: List[EthAccount]
            ):
        
        alloc_mgr = AllocationManager()
        for contract in contracts:
            contract_adr = RescaleFreenetGenesis.contract_address(contract)
            alloc_mgr.add_item(AllocationItem(
                address=contract_adr,
                balance="0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                storage={}
            ))
        
        hf_mgr = HardForkManager()
        hf_mgr.add_fork(HardForkItem("homesteadBlock", 0))
        hf_mgr.add_fork(HardForkItem("daoForkBlock", 0))
        hf_mgr.add_fork(HardForkItem("eip150Block", 0))
        hf_mgr.add_fork(HardForkItem("eip155Block", 0))
        hf_mgr.add_fork(HardForkItem("eip158Block", 0))
        hf_mgr.add_fork(HardForkItem("byzantiumBlock", 0))
        hf_mgr.add_fork(HardForkItem("constantinopleBlock", 0))
        hf_mgr.add_fork(HardForkItem("petersburgBlock", 0))
        hf_mgr.add_fork(HardForkItem("istanbulBlock", 0))
        hf_mgr.add_fork(HardForkItem("muirGlacierBlock", 0))
        hf_mgr.add_fork(HardForkItem("muirGlacierBlock", 0))
        hf_mgr.add_fork(HardForkItem("berlinBlock", 0))
        hf_mgr.add_fork(HardForkItem("londonBlock", 0))
        hf_mgr.add_fork(HardForkItem("arrowGlacierBlock", 0))
        hf_mgr.add_fork(HardForkItem("grayGlacierBlock", 0))
        hf_mgr.add_fork(HardForkItem("parisBlock", 0))
        hf_mgr.add_fork(HardForkItem("shanghaiTime", 0))
        hf_mgr.add_fork(HardForkItem("cancunTime", 0))

        qbft = QbftConsensusItem(
            validators=[e.eth_address for e in validators],
            block_period_seconds=2,
            epoch=30000,
            request_timeout_seconds=10
        )

        cfg_mgr = ConfigManager(
            hard_forks=hf_mgr,
            consensus=qbft,
            chain_id=1337,
            contract_size_limit=2147483647,
            zero_base_fee=True
            )
        
        self.gen_mgr = GenesisManager(
            difficulty="0",
            gas_limit="0x1fffffffffffff",
            mix_hash="0x0000000000000000000000000000000000000000000000000000000000000000",
            nonce="0x0000000000000000",
            timestamp="0x0",
            coinbase="0x0000000000000000000000000000000000000000",
            alloc_manager=alloc_mgr,
            config_manager=cfg_mgr
        )
    
    def to_dict(self):
        return self.gen_mgr.to_dict()
