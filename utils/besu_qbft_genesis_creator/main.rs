use ethaddr::Address;
use hex;
use std::fs;
use std::io::{self, Read, Write};
use std::env;
use rlp::{RlpStream};
use serde_json::{Value, json};

fn main() -> io::Result<()> {

    let mut template_file = fs::File::open("/sources/template.json")?;
    let mut template_contents = String::new();
    template_file.read_to_string(&mut template_contents)?;
    let mut json: Value = serde_json::from_str(&template_contents)?;

    let validators = read_validators()?;
    let extra_data = encode_extra_data(&validators);
    let alloc = read_contracts()?;

    json["extraData"] = json!(format!("0x{}", extra_data));
    json["alloc"] = json!(alloc);

    let output = serde_json::to_string_pretty(&json)?;
    let mut output_file = fs::File::create("/output/genesis.json")?;
    output_file.write_all(output.as_bytes())?;

    Ok(())
}

fn to_checksum_address(address: &str) -> Result<String, String> {
    let address = address.strip_prefix("0x").unwrap_or(address);
    let bytes = hex::decode(address).map_err(|e| format!("Invalid hex string: {}", e))?;
    if bytes.len() != 20 {
        return Err(format!("Invalid address length: expected 20 bytes, got {}", bytes.len()));
    }
    let address = Address::from_slice(&bytes);
    Ok(address.to_string())
}

fn calculate_contract_address(contract_name: &str) -> io::Result<String> {
    let address_hex = hex::encode(format!("Rescale{}", contract_name));
    let contract_address = if address_hex.len() >= 40 {
        address_hex[..40].to_string()
    } else {
        format!("{:0>40}", address_hex)
    };
    to_checksum_address(&format!("0x{}", contract_address)).map_err(|e| io::Error::new(io::ErrorKind::Other, e))
}

fn read_contracts() -> io::Result<Value> {
    let contracts_env = env::var("CONTRACTS").expect("CONTRACTS environment variable not set");
    let contract_names: Vec<&str> = contracts_env.split(',').map(|s| s.trim()).collect();
    let mut alloc = json!({});
    for contract_name in contract_names {
        let address = calculate_contract_address(contract_name)?;
        let address_file_path = format!("/output/{}.address", contract_name);
        fs::write(&address_file_path, &address)?;
        
        let bin_runtime_path = format!("/contracts/{}.bin-runtime", contract_name);
        let mut file = fs::File::open(bin_runtime_path)?;
        let mut contents = String::new();
        file.read_to_string(&mut contents)?;
        
        let value = serde_json::json!({
            "balance": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            "code": contents.trim(),
            "storage": {}
        });
        alloc[address] = value;
    }
    Ok(alloc)
}

fn read_validators() -> io::Result<Vec<String>> {
    let validators_env = env::var("VALIDATORS").expect("VALIDATORS environment variable not set");
    let validator_names: Vec<&str> = validators_env.split(',').map(|s| s.trim()).collect();
    let mut validators = Vec::new();
    for validator in validator_names {
        let address_path = format!("/validators/{validator}/.address");
        let mut file = fs::File::open(address_path)?;
        let mut contents = String::new();
        file.read_to_string(&mut contents)?;
        validators.push(contents.trim().to_string());
    }
    Ok(validators)
}

fn encode_extra_data(validators: &[String]) -> String {
    let mut rlp = RlpStream::new_list(5);
    rlp.append(&vec![0u8; 32]); // Vanity data (32 bytes)
    rlp.begin_list(validators.len()); // Validators
    for validator in validators {
        let address = hex::decode(&validator[2..]).unwrap();
        rlp.append(&address);
    }
    rlp.append_raw(&[0xc0], 1); // No vote (empty list)
    rlp.append(&0u8); // Round number (0)
    rlp.append_raw(&[0xc0], 1); // Seals (empty list)
    hex::encode(rlp.out().as_ref())
}