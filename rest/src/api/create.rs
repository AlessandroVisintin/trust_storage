use crate::ipfs::ipfs_api::IPFSApi;
use crate::ipfs::types::create::ItemData;
use crate::{ipfs::IPFSClient, jwt::payload::Payload};
use ntex::web;
use serde_json::json;
use std::fmt;

use crate::jwt;

pub async fn create(data: web::types::Json<Item>) -> impl web::Responder {
    match jwt::verify(data.get_jwt(), data.get_public_key()) {
        Ok(payload) => {
            let result = create_ipfs_file(payload, data.get_jwt(), data.get_public_key()).await;
            web::HttpResponse::Ok().json(&result)
        }
        Err(error) => web::HttpResponse::BadRequest().json(&error),
    }
}

async fn create_ipfs_file(payload: Payload, jwt: String, public_key: String) -> serde_json::Value {
    let client =
        IPFSClient::new(std::env::var("IPFS_URL").unwrap_or("http://localhost:5001".to_string()));

    let result = client
        .create(
            ItemData::new(payload.get_tbom().unwrap(), jwt.clone(), public_key.clone()),
            Default::default(),
        )
        .await;
    match result {
        Ok(response) => json!({ "result": "ok", "response": response }),
        Err(error) => json!({ "payload": "ko", "error": error.to_string() }),
    }
}

#[derive(serde::Deserialize)]
pub struct Item {
    jwt: String,
    public_key: String,
}

impl Item {
    pub fn get_jwt(&self) -> String {
        self.jwt.clone()
    }

    pub fn get_public_key(&self) -> String {
        self.public_key.clone()
    }
}

impl fmt::Display for Item {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} {}", self.jwt, self.public_key)
    }
}
