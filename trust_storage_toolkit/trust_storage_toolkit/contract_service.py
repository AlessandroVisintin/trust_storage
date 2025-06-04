import solcx
from pathlib import Path

from .models import Contract


class ContractService:
    
    def __init__(self, solc_version: str = "0.8.19"):
        self.solc_version = solc_version
        self._ensure_solc_installed()
    
    def _ensure_solc_installed(self):
        installed_versions = [str(v) for v in solcx.get_installed_solc_versions()]
        if self.solc_version not in installed_versions:
            solcx.install_solc(self.solc_version)
    
    def compile(self, source_path: Path) -> Contract:
        if not source_path.exists():
            raise FileNotFoundError(f"Contract file {source_path} not found")
        
        compiled = solcx.compile_files(
            [str(source_path)],
            output_values=["abi", "bin", "bin-runtime"],
            solc_version=self.solc_version
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
    
    def calculate_contract_address(self, contract_name: str) -> str:
        return f"0x{contract_name.encode().hex()[:40].ljust(40, '0')}"
