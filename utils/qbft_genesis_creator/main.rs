use ethaddr::Address;
use std::fs::{self, File};
use std::io::{BufRead, BufReader, Read, Write};
use std::path::Path;
use rlp::{RlpStream};
use serde_json::{Value, json};


fn main() -> Result<(), Box<dyn std::error::Error>>  {

    let mut json_content = read_json("/sources/template.json")?;
    let mut json_obj = json_content.as_object_mut().ok_or("JSON is not an object")?;

    let bootnodes = read_bootnodes("/sources/bootnodes.txt");
    let enodes: Vec<String> = bootnodes.iter()
        .map(|(pubkey, address)| generate_enode(pubkey, address))
        .collect();
    json_obj["bootnodes"] = json!(enodes);

    let validators = read_validators("/sources/validators.txt");
    let extradata = generate_extradata(&validators);
    json_obj["extraData"] = json!(format!("0x{}", extradata));

    let contracts = read_contracts("/sources/contracts");
    json_obj["alloc"] = generate_alloc(contracts);

    write_json("/output/genesis.json", &json!(json_obj))?;
    println!("genesis.json have been successfully generated");

    Ok(())

}

fn read_json(file_location: &str) -> Result<Value, Box<dyn std::error::Error>> {
    let mut json_file = File::open(file_location)?;
    let mut json_content = String::new();
    json_file.read_to_string(&mut json_content)?;
    Ok(serde_json::from_str(&json_content)?)
}

fn write_json(file_location: &str, json_content: &Value) -> Result<(), Box<dyn std::error::Error>> {
    let output = serde_json::to_string_pretty(&json_content)?;
    let mut output_file = File::create(file_location)?;
    output_file.write_all(output.as_bytes())?;
    Ok(())
}

fn read_bootnodes(file_location: &str) -> Vec<(String, String)> {
    let file_path = Path::new(file_location);
    let file = File::open(file_path).expect("Failed to open bootnodes.txt");
    let reader = BufReader::new(file);
    reader.lines()
        .filter_map(|line| {
            let line = line.expect("Error reading line").trim().to_string();
            if line.is_empty() {
                return None;
            }
            let mut parts = line.split('@');
            match (parts.next(), parts.next(), parts.next()) {
                (Some(pubkey), Some(address), None) => {
                    let clean_pubkey = pubkey.trim()
                        .strip_prefix("0x")
                        .unwrap_or(pubkey.trim())
                        .to_string();
                    let clean_address = address.trim().to_string();
                    Some((clean_pubkey, clean_address))
                }
                _ => {
                    eprintln!("Invalid format in bootnode entry: {}", line);
                    None
                }
            }
        })
        .collect()
}

fn read_validators(file_location: &str) -> Vec<String> {
    let file_path = Path::new(file_location);
    let file = File::open(file_path).expect("Failed to open validators.txt");
    let reader = BufReader::new(file);
    reader.lines()
        .map(|line| {
            line.expect("Error reading line")
                .trim()
                .strip_prefix("0x")
                .unwrap_or_default()
                .to_string()
        })
        .filter(|s| !s.is_empty())
        .collect()
}

fn read_contracts(folder_location: &str) -> Vec<(String, String)> {
    let contracts_dir = Path::new(folder_location);
    fs::read_dir(contracts_dir)
        .map(|entries| {
            entries
                .filter_map(Result::ok)
                .filter(|entry| entry.path().extension().and_then(|s| s.to_str()) == Some("bin-runtime"))
                .filter_map(|entry| {
                    let path = entry.path();
                    let file_name = path.file_stem()?.to_str()?.to_string();
                    let mut content = String::new();
                    fs::File::open(&path).ok()?.read_to_string(&mut content).ok()?;
                    Some((file_name, content.trim().to_string()))
                })
                .collect()
        })
        .unwrap_or_default()
}

fn generate_enode(node_pubkey: &str, node_address: &str) -> String {
    format!(
        "enode://{}@{}",
        node_pubkey.trim().strip_prefix("0x").unwrap_or(node_pubkey.trim()),
        node_address
    )
}

fn generate_extradata(validators: &[String]) -> String {
    let mut rlp = RlpStream::new_list(5);
    rlp.append(&vec![0u8; 32]); // Vanity data (32 bytes)
    rlp.begin_list( validators.len() ); // Validators
    for validator in validators {
        let address = validator.strip_prefix("0x").unwrap_or(validator);
        let decoded = hex::decode(address).expect("Invalid hexadecimal address");
        assert_eq!(decoded.len(), 20, "Validator address must be 20 bytes");
        rlp.append(&decoded);
    }
    //rlp.append_raw(&[0xc0], 1); // No vote (empty list)
    rlp.append_empty_data();
    //rlp.append(&0u8); // Round number (0)
    rlp.append(&0u64);
    //rlp.append_raw(&[0xc0], 1); // Seals (empty list)
    rlp.append_empty_data();
    hex::encode( rlp.out() )
}

fn to_checksum_address(address: &str) -> String {
    let address = address.strip_prefix("0x").unwrap_or(address);
    let bytes = hex::decode(address).expect("Invalid hex string");
    assert_eq!(bytes.len(), 20, "Invalid address length");
    Address::from_slice(&bytes).to_string()
}

fn calculate_contract_address(contract_name: &str) -> String {
    let address_hex = hex::encode(format!("Rescale{}", contract_name));
    let contract_address = if address_hex.len() >= 40 {
        address_hex[..40].to_string()
    } else {
        format!("{:0>40}", address_hex)
    };
    to_checksum_address(&format!("0x{}", contract_address))
}

fn generate_alloc(contracts: Vec<(String, String)>) -> Value {
    let mut alloc = json!({});
    for (contract_name, bytecode) in contracts {
        let address = calculate_contract_address(&contract_name);
        let contract_data = json!({
            "balance": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            "code": bytecode.trim(),
            "storage": {}
        });
        alloc[address] = contract_data;
    }
    alloc
}