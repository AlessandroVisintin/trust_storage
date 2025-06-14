import json
from typing import Dict, List, Any

from .base_contract import BaseContract
from .simple_storage import SimpleStorage


class ContractFactory:

    def __init__(self, manifest_path: str, node_url: str):
        self.node_url = node_url
        with open(manifest_path, 'r') as f:
            self._manifest: Dict[str, Any] = json.load(f)

        self._class_map: Dict[str, type[BaseContract]] = {
            "SimpleStorage": SimpleStorage
        }

    def get_contract(self, name: str) -> BaseContract:
        if name not in self._manifest:
            raise ValueError(f"Contract '{name}' not found in manifest file.")
        
        if name not in self._class_map:
            raise ValueError(f"Adapter class for contract '{name}' is not registered in the factory.")

        contract_info = self._manifest[name]
        contract_class = self._class_map[name]
        
        return contract_class(
            contract_address=contract_info['address'],
            abi=contract_info['abi'],
            node_url=self.node_url
        )
