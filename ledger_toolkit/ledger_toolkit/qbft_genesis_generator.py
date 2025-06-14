# generators/genesis_generator.py
import json
from pathlib import Path
from typing import Dict, Any, List

from .base_generator import BaseGenerator
from .config_models import NetworkConfig
from .contract_service import ContractService
from .account_service import AccountService

from .ledger_utils import calculate_qbft_extradata, calculate_contract_address


class QbftGenesisGenerator(BaseGenerator):
    
    def __init__(
            self,
            account_service: AccountService,
            base_path: Path,
            contract_service: ContractService,
            genesis_template_path: Path
            ):
        super().__init__(account_service, base_path)
        self.contract_service = contract_service
        self.genesis_template_path = genesis_template_path
    
    def generate(self, config: NetworkConfig) -> None:
        if not config.consensus.name == "qbft":
            raise ValueError("Configuration consensus is not QBFT")
        genesis = self._load_template(self.genesis_template_path)
        genesis["config"]["qbft"] = config.consensus.parameters
        if config.contracts:
            genesis["alloc"] = self._process_contracts(config.contracts)
        validators = self._collect_validators(config)
        genesis["extraData"] = calculate_qbft_extradata(validators)
        
        self._write_genesis_file(genesis)
    
    def _load_template(self, template_path: Path) -> Dict[str, Any]:
        with open(template_path, 'r') as f:
            return json.load(f)
    
    def _process_contracts(self, contracts_config) -> Dict[str, Any]:
        alloc = {}
        contracts_path = self.base_path / Path(contracts_config.path)
        
        for contract_name in contracts_config.members:
            contract_file = contracts_path / f"{contract_name}.sol"
            
            if not contract_file.exists():
                raise FileNotFoundError(f"Contract {contract_file} not found")
            
            compiled_contract = self.contract_service.compile(contract_file)
            contract_address = calculate_contract_address(contract_name)
            
            alloc[contract_address] = {
                "balance": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "code": compiled_contract.bin_runtime,
                "storage": {}
            }
        
        return alloc
    
    def _collect_validators(self, config: NetworkConfig) -> List[str]:
        validators = []
        for service in config.services.values():
            if service.node_config.is_validator:
                validators.append(self.account_service.get_address_by_name(service.name))
        return validators
    
    def _write_genesis_file(self, genesis: Dict[str, Any])-> None:
        output_path = self.base_path / "genesis.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(genesis, f, indent=2)
