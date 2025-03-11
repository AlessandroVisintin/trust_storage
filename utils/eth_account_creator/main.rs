use secp256k1::{Secp256k1, SecretKey, PublicKey};
use rand::Rng;
use sha3::{Digest, Keccak256};
use std::env;
use std::fs::{self, File};
use std::io::Write;
use std::path::Path;


fn main() {
    let output_dir = Path::new("/output");
    if !output_dir.exists() {
        fs::create_dir_all(output_dir).expect("Failed to create output directory");
    }
    let secp = Secp256k1::new();
    let mut rng = rand::thread_rng();
    loop {

        let secret_key_bytes: [u8; 32] = rng.r#gen();
        let secret_key = SecretKey::from_slice(&secret_key_bytes).expect("32 bytes, within curve order");
        let public_key = PublicKey::from_secret_key(&secp, &secret_key);
        let private_key_hex = format!("0x{}", hex::encode(secret_key_bytes));
        let public_key_bytes = public_key.serialize_uncompressed();
        let public_key_hex = format!("0x{}", hex::encode(&public_key_bytes[1..]));
        let public_key_hash = Keccak256::digest(&public_key_bytes[1..]);
        let eth_address = &public_key_hash[12..];
        let eth_address_hex = format!("0x{}", hex::encode(eth_address));

        let folder_name = &eth_address_hex[(eth_address_hex.len() - 8)..];
        let account_dir = output_dir.join(folder_name);
        if account_dir.exists() {
            println!("Account directory {} already exists, regenerating...", folder_name);
            continue;
        }
        fs::create_dir(&account_dir).expect("Failed to create account directory");
        let mut prv_file = File::create(account_dir.join(".prv")).expect("Failed to create .prv");
        let mut pub_file = File::create(account_dir.join(".pub")).expect("Failed to create .pub");
        let mut adr_file = File::create(account_dir.join(".address")).expect("Failed to create .address");
        prv_file.write_all(private_key_hex.as_bytes()).expect("Failed to write .prv");
        pub_file.write_all(public_key_hex.as_bytes()).expect("Failed to write .pub");
        adr_file.write_all(eth_address_hex.as_bytes()).expect("Failed to write address");
        println!("Generated keys for {}", folder_name);
        break;
    }
}
