import yaml
from pathlib import Path
from typing import List, Any

from .accounts import AccountRepository, AccountGenerator
from .besu_network import BesuNode, BesuPermissions
from .contracts import ContractRepository
from .eth_network import EthNode, EthEndpoints
from .qbft_network import QbftNode

        
class Besu20250531ServiceLoader:
    IMAGE = "harbor.rescale-project.eu/rescale-all/besu:2025-05-31"

    @staticmethod
    def handles_image(image: str) :
        return image == Besu20250531ServiceLoader.IMAGE
    
    @staticmethod
    def load_service(compose_path: Path, service_name: str, service_data: dict):

        account_path = None
        for volume in service_data["volumes"]:
            if volume.endswith(":/sources/account"):
                account_path = volume.split(":/sources/account")[0]

        account_dir = compose_path.parent / Path(account_path).parent
        account_repo = AccountRepository(account_dir)
        account_name = account_dir.name
        if not account_repo.load(account_name):
            new_account = AccountGenerator.generate(service_name)
            account_repo.save(new_account)
        account = account_repo.load(service_name)

        p2p_endpoint = None
        rpc_endpoint = None
        for port in service_data["ports"]:
            if port.endswith(":8545"):
                rpc_endpoint = port.split(":8545")[0]
            if port.endswith(":30303"):
                p2p_endpoint = port.split(":30303")[0]
        if not p2p_endpoint or not rpc_endpoint:
            raise ValueError(f"Missing required port mappings in {service_name}")

        eth_node = EthNode(
            account=account,
            endpoints=EthEndpoints(
                rpc_endpoint=f"http://{rpc_endpoint}",
                p2p_endpoint=f"enode://{account.public_key.strip('0x')}@{p2p_endpoint}"
            )
        )
        
        besu_perms = BesuPermissions(
            account_permissions=service_data.get("x-node-config", []).get("account-permissions", []),
            node_permissions=service_data.get("x-node-config", {}).get("node-permissions", [])
        )
        
        besu_node = BesuNode(
            eth_node=eth_node,
            is_bootnode=service_data.get("x-node-config", {}).get("is_bootnode", False),
            permissions=besu_perms
        )
        
        qbft_node = QbftNode(
            besu_node=besu_node,
            is_validator=service_data.get("x-node-config", {}).get("is_validator", False)
        )

        return qbft_node


class BesuComposeLoader:

    SERVICE_LOADERS = [
        Besu20250531ServiceLoader
    ]

    @staticmethod
    def find_service_loader(image: str):
        for loader in BesuComposeLoader.SERVICE_LOADERS:
            if loader.handles_image(image):
                return loader
        return None

    def __init__(self, compose_path: str):
        self.compose_path = Path(compose_path)
        if not self.compose_path.exists():
            raise FileNotFoundError(f"Compose file {compose_path} not found")

        with self.compose_path.open('r') as f:
            self.compose_data = yaml.safe_load(f)

    def parse_contracts_config(self) -> ContractRepository:
        contracts_config = self.compose_data["x-network-config"]["contracts"]
        contracts_path = Path(contracts_config["path"])
        contracts_repository = ContractRepository(self.compose_path.parent / contracts_path)
        for member in contracts_config["members"]:
            contracts_repository.load(member["name"])
        return contracts_repository

    def parse_services_config(self) -> List[Any]:
        services_config = self.compose_data["services"]
        services = []
        for service_name, service_data in services_config.items():
            image = service_data["image"]
            loader = BesuComposeLoader.find_service_loader(image)    
            if not loader:
                raise ValueError(f"Cannot find loader for image {image}")
            services.append(
                loader.load_service(
                    self.compose_path,
                    service_name,
                    service_data
                    )
                )
        return services
