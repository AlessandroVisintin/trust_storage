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

def generate_private_key() -> str:
    private_key_bytes = secrets.randbits(256).to_bytes(32, 'big')
    return '0x' + private_key_bytes.hex()

def derive_public_key(private_key: str) -> str:
    private_key_bytes = bytes.fromhex(private_key[2:])
    signing_key = SigningKey.from_string(
        private_key_bytes,
        curve=SECP256k1
        )
    public_key_bytes = signing_key.get_verifying_key().to_string()
    return '0x' + public_key_bytes.hex()

def derive_address(public_key: str) -> str:
    public_key_bytes = bytes.fromhex(public_key[2:])
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(public_key_bytes)
    address_bytes = keccak_hash.digest()[-20:]
    return to_checksum_address('0x' + address_bytes.hex())

def get_extradata(validators) -> str:
    vanity = b'\x00' * 32 
    decoded = [bytes.fromhex( v.strip("0x") ) for v in validators]
    vote = []
    round_number = 0
    seals = []
    payload = [vanity, decoded, vote, round_number, seals]
    return f"0x{ rlp.encode(payload).hex() }"