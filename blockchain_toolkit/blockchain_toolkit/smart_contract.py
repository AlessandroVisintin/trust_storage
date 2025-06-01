import os
import json
import solcx
from dataclasses import dataclass, asdict
from pathlib import Path

from .eth_utils import to_checksum_address

@dataclass
class SmartContract:
    name: str
    abi: dict
    bin: str
    bin_runtime: str


class SmartContractCompiler:
    
    @staticmethod
    def compile(contract_name: str, contracts_dir: str, solc_version: str = "0.8.19") -> SmartContract:
        solc_versions = [str(v) for v in solcx.get_installed_solc_versions()]
        if solc_version not in solc_versions:
            solcx.install_solc(solc_version)

        contract_file = Path(contracts_dir) / f"{contract_name}.sol"
        if not contract_file.exists():
            raise FileNotFoundError(f"Contract file {contract_file} not found")
        
        compiled = solcx.compile_files(
            [str(contract_file)],
            output_values=["abi", "bin", "bin-runtime"],
            solc_version=solc_version
        )
        
        contract_key = list(compiled.keys())[0]
        contract_data = compiled[contract_key]
        
        return SmartContract(
            name=contract_name,
            abi=contract_data['abi'],
            bin=contract_data['bin'],
            bin_runtime=contract_data['bin-runtime']
        )


class SmartContractLoader:
    @staticmethod
    def load(filepath: str) -> SmartContract:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return SmartContract(
            name=data['name'],
            abi=data['abi'],
            bin=data['bin'],
            bin_runtime=data['bin_runtime']
        )
    
    @staticmethod
    def dump(contract: SmartContract, filepath: str) -> None:
        with open(filepath, 'w') as f:
            json.dump(asdict(contract), f, indent=2)


class SmartContractRepository:
    
    def __init__(self, folderpath: str):
        self.folderpath = folderpath
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
    
    def is_compiled(self, contract_name:str, contracts_dir:str=None) -> bool:
        contracts_dir = contracts_dir if contracts_dir else self.folderpath
        filename = f"{contract_name}.json"
        contract_path = os.path.join(self.folderpath, filename)
        return os.path.exists(contract_path)
    
    def compile(self, contract_name:str, contracts_dir:str=None, solc_version: str = "0.8.19") -> None:
        contracts_dir = contracts_dir if contracts_dir else self.folderpath
        contract = SmartContractCompiler.compile(contract_name, contracts_dir, solc_version)
        filename = f"{contract_name}.json"
        SmartContractLoader.dump(contract, os.path.join(self.folderpath, filename))
    
    def get(self, contract_name: str) -> SmartContract:
        filepath = os.path.join(self.folderpath, f"{contract_name}.json")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Contract {contract_name} not found")
        return SmartContractLoader.load(filepath)
    
    def remove(self, contract_name: str) -> SmartContract:
        filepath = os.path.join(self.folderpath, f"{contract_name}.json")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Contract {contract_name} not found")
        contract = SmartContractLoader.load(filepath)
        os.remove(filepath)
        return contract
