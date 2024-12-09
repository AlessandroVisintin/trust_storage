use crate::ipfs::types::create::Options;
use crate::ipfs::types::create::Response;
use crate::ipfs::types::error::Error;

use super::types::create::ItemData;

pub trait IPFSApi {
    async fn create(&self, data: ItemData, options: Options) -> Result<Response, Error>;
    async fn cat(
        &self,
        arg: String,
        offset: Option<i64>,
        length: Option<i64>,
        progess: Option<bool>,
    ) -> Result<serde_json::Value, Error>;
    async fn pin_rm(
        &self,
        arg: String,
        recursive: Option<bool>,
    ) -> Result<serde_json::Value, Error>;
}
