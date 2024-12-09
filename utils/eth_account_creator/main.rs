use secp256k1::{Secp256k1, SecretKey, PublicKey};
use rand::Rng;
use sha3::{Digest, Keccak256};
use std::env;
use std::fs::{File, create_dir_all};
use std::io::Write;
use std::path::Path;

fn main() {

    let secp = Secp256k1::new();
    let mut rng = rand::thread_rng();

    let accounts = env::var("ACCOUNTS").expect("ACCOUNTS environment variable not set");
    let account_names: Vec<&str> = accounts.split(',').collect();

    for account_name in account_names {
        let account_name = account_name.trim();
        let output_dir = Path::new("/output").join(account_name);
        create_dir_all(&output_dir).expect("Failed to create output directory");

        let secret_key_bytes: [u8; 32] = rng.gen();

        let secret_key = SecretKey::from_slice(&secret_key_bytes).expect("32 bytes, within curve order");
        let public_key = PublicKey::from_secret_key(&secp, &secret_key);

        let private_key_hex = format!("0x{}", hex::encode(secret_key_bytes));
        let public_key_bytes = public_key.serialize_uncompressed();
        let public_key_hex = format!("0x{}", hex::encode(&public_key_bytes[1..]));

        let public_key_hash = Keccak256::digest(&public_key_bytes[1..]);
        let eth_address = &public_key_hash[12..];
        let eth_address_hex = format!("0x{}", hex::encode(eth_address));

        let mut prv_file = File::create(output_dir.join(".prv")).expect("Failed to create private key file");
        let mut pub_file = File::create(output_dir.join(".pub")).expect("Failed to create public key file");
        let mut address_file = File::create(output_dir.join(".address")).expect("Failed to create address file");
        prv_file.write_all(private_key_hex.as_bytes()).expect("Failed to write private key");
        pub_file.write_all(public_key_hex.as_bytes()).expect("Failed to write public key");
        address_file.write_all(eth_address_hex.as_bytes()).expect("Failed to write address");

        println!("Generated keys for account: {}", account_name);
    
    }
}