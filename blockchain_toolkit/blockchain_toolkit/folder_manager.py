import os
import yaml
from pathlib import Path
from typing import Dict, Any, List

from .eth_account import EthAccountRepository
from .eth_utils import to_checksum_address


class BaseStrategy:

    def execute(self, config_path: str) -> None:
        raise NotImplementedError


# class BootnodesManager:
#     def __init__(self, bootnodes: List[Dict[str, Any]], base_path: Path):
#         self.bootnodes = bootnodes
#         self.base_path = base_path / "bootnodes"
#         self.base_path.mkdir(exist_ok=True)

#     def dump(self):

#         with open(self.base_path / "bootnodes.txt", "w") as f:
#             for item in self.bootnodes:
#                 f.write(f"{item['name']}\n")


# class ValidatorsManager:
#     def __init__(self, validators: List[Dict[str, Any]], base_path: Path):
#         self.validators = validators
#         self.base_path = base_path / "validators"
#         self.base_path.mkdir(exist_ok=True)

#     def dump(self):
#         # JSON array of validator names
#         import json
#         data = [v["name"] for v in self.validators]
#         with open(self.base_path / "validators.json", "w") as f:
#             json.dump(data, f, indent=2)


# class PermissionsManager:
#     def __init__(self, perms: List[Dict[str, Any]], base_path: Path):
#         self.perms = perms
#         self.base_path = base_path / "permissions"
#         self.base_path.mkdir(exist_ok=True)

#     def dump(self):
#         # One file per node: node-<name>.permissions.json
#         import json
#         for item in self.perms:
#             fn = f"node-{item['name']}.permissions.json"
#             with open(self.base_path / fn, "w") as f:
#                 json.dump(item, f, indent=2)


class Besu20250531Strategy(BaseStrategy):
    
    REQUIRED_TAG = "besu:2025-05-31"

    def execute(self, config_path: str) -> None:
        cfg = yaml.safe_load(Path(config_path).read_text())
        name = cfg["name"]
        image = cfg["image"]
        if not image.endswith(f"{self.REQUIRED_TAG}"):
            raise ValueError(f"Config image '{image}' must end with {self.REQUIRED_TAG}")

        root = Path(config_path).parent / name
        root.mkdir(exist_ok=True)

        nodes_cfg = cfg.get("nodes", [])
        repo = EthAccountRepository(str(root / "nodes"))
        for node in nodes_cfg:
            repo.generate(name=node["name"])

        # # 2) Dump bootnodes
        # BootnodesManager(cfg.get("bootnodes", []), root).dump()

        # # 3) Dump validators
        # ValidatorsManager(cfg.get("validators", []), root).dump()

        # # 4) Dump node-permissions & account-permissions
        # PermissionsManager(cfg.get("node-permissions", []), root).dump()
        # PermissionsManager(cfg.get("account-permissions", []), root).dump()

        # # 5) Write docker-compose.yml with updated volume mounts
        # compose = {
        #     "version": "3.7",
        #     "services": {
        #         name: {
        #             "image": image,
        #             "volumes": [
        #                 f"./nodes:/app/nodes",
        #                 f"./bootnodes:/app/bootnodes",
        #                 f"./validators:/app/validators",
        #                 f"./permissions:/app/permissions",
        #             ],
        #             "ports": [
        #                 cfg_item["rpc-endpoint"] + ":8545" 
        #                 for cfg_item in nodes_cfg
        #             ] + [
        #                 cfg_item["p2p-endpoint"] + ":30303" 
        #                 for cfg_item in nodes_cfg
        #             ]
        #         }
        #     }
        # }
        # with open(root / "docker-compose.yml", "w") as f:
        #     yaml.safe_dump(compose, f, sort_keys=False)

        # print(f"Besu20250531 layout created in {root}")

if __name__ == "__main__" :

    folder_strategy = Besu20250531Strategy()
    folder_strategy.execute("./besu_networks/test.yml")