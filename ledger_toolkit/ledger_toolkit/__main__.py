import argparse
from pathlib import Path

from .account_service import AccountService
from .contract_service import ContractService
from .config_parser import ConfigParser
from .bootnode_generator import BootnodeGenerator
from .permissions_generator import PermissionsGenerator
from .private_key_generator import PrivateKeyGenerator
from .qbft_genesis_generator import QbftGenesisGenerator


parser = argparse.ArgumentParser("ledger_toolkit")
parser.add_argument("compose_path", help="Path to the docker-compose.yml to parse", type=str)
parser.add_argument("genesis_template_path", help="Path to genesis.json template", type=str)
args = parser.parse_args()

compose_path = Path(args.compose_path)
genesis_template_path = Path(args.genesis_template_path)
account_service = AccountService()
contract_service = ContractService()

config = ConfigParser().parse(compose_path)

BootnodeGenerator(account_service, compose_path.parent).generate(config)
PermissionsGenerator(account_service, compose_path.parent).generate(config)
PrivateKeyGenerator(account_service, compose_path.parent).generate(config)
QbftGenesisGenerator(account_service, compose_path.parent, contract_service, genesis_template_path).generate(config)
        
print("Network configuration generated successfully!")
