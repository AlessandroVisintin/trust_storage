import json
import solcx
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Contract:
    name: str
    abi: dict
    bin: str
    bin_runtime: str


class ContractCompiler:
    
    @staticmethod
    def compile(source_path: str, solc_version: str = "0.8.19") -> Contract:
        source_path = Path(source_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Contract file {source_path} not found")
        
        solc_versions = [str(v) for v in solcx.get_installed_solc_versions()]
        if solc_version not in solc_versions:
            solcx.install_solc(solc_version)
        
        compiled = solcx.compile_files(
            [str(source_path)],
            output_values=["abi", "bin", "bin-runtime"],
            solc_version=solc_version
        )

        contract_name = source_path.stem
        contract_key = next(
            k for k in compiled.keys() if k.endswith(f":{contract_name}")
        )
        contract_data = compiled[contract_key]
        return Contract(
            name=contract_name,
            abi=contract_data['abi'],
            bin=contract_data['bin'],
            bin_runtime=contract_data['bin-runtime']
        )


class ContractRepository:

    def __init__(self, folderpath: str):
        self.folderpath = Path(folderpath)
        self.folderpath.mkdir(parents=True, exist_ok=True)

    def save(self, contract: Contract) -> None:
        file_path = self.folderpath / f"{contract.name}.json"
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(asdict(contract), f, ensure_ascii=False, indent=2)

    def load(self, name: str, compile: bool = True) -> Contract:
        file_path = self.folderpath / f"{name}.json"
        if file_path.exists():
            with file_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
            return Contract(**data)
                
        if compile:
            source_path = (self.folderpath / f"{name}.sol").resolve()
            contract = ContractCompiler.compile(source_path)
            self.save(contract)
            return contract

        raise FileNotFoundError(f"{file_path} not found")
