from pathlib import Path

from .crypto_service import CryptoService
from .contract_service import ContractService
from .config_parser import ConfigParser
from .bootnode_generator import BootnodeGenerator
from .permissions_generator import PermissionsGenerator
from .private_key_generator import PrivateKeyGenerator
from .genesis_generator import GenesisGenerator

class NetworkGenerator:
    """Main orchestrator for generating blockchain network configurations."""
    
    def __init__(self):
        self.crypto_service = CryptoService()
        self.contract_service = ContractService()
        self.config_parser = ConfigParser()
    
    def generate_network(self, compose_path: Path, genesis_template_path: Path) -> None:

        # Parse configuration
        config = self.config_parser.parse(compose_path)

        # Initialize generators
        self.bootnode_generator = BootnodeGenerator(self.crypto_service, compose_path.parent)
        self.permissions_generator = PermissionsGenerator(self.crypto_service, compose_path.parent)
        self.private_key_generator = PrivateKeyGenerator(self.crypto_service, compose_path.parent)
        self.genesis_generator = GenesisGenerator(self.crypto_service, self.contract_service, compose_path.parent)
        
        # Generate all required files
        self.bootnode_generator.generate(config)
        self.permissions_generator.generate(config)
        self.private_key_generator.generate(config)
        
        # Generate genesis file
        genesis_output_path = compose_path.parent / "genesis.json"
        self.genesis_generator.generate(config, genesis_template_path, genesis_output_path)
        
        print("Network configuration generated successfully!")
