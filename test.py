# from blockchain_toolkit.compose_loader import BesuComposeLoader

# yaml_file = "besu_networks/localnode/docker-compose.yml"
# loader = BesuComposeLoader(yaml_file)

# print(
#     loader.parse_services_config()
# )

from pathlib import Path
from trust_storage_toolkit.network_generator import NetworkGenerator


generator = NetworkGenerator()
generator.generate_network(
    compose_path=Path("besu_networks\localnode\docker-compose.yml"),
    genesis_template_path=Path("besu_networks\qbft_genesis_template.json")
)
