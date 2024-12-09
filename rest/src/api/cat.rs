use crate::ipfs::ipfs_api::IPFSApi;
use crate::ipfs::IPFSClient;
use ntex::web;

pub async fn cat(hash: web::types::Path<String>) -> impl web::Responder {
    let client =
        IPFSClient::new(std::env::var("IPFS_URL").unwrap_or("http://localhost:5001".to_string()));

    let result = client.cat(hash.to_string(), None, None, None).await;
    match result {
        Ok(response) => web::HttpResponse::Ok().json(&response),
        Err(error) => {
            web::HttpResponse::BadRequest().json(&serde_json::json!({ "error": error.to_string() }))
        }
    }
}
