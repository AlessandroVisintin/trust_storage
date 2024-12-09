use ipfs_api::IPFSApi;
use types::create::ItemData;

pub mod ipfs_api;
pub mod types;

pub struct IPFSClient {
    uri: String,
}

impl IPFSClient {
    pub fn new(uri: String) -> Self {
        IPFSClient { uri }
    }
}

impl IPFSApi for IPFSClient {
    async fn create(
        &self,
        data: ItemData,
        options: types::create::Options,
    ) -> Result<types::create::Response, types::error::Error> {
        // Parse the URI
        let base_uri = self.uri.clone() + "/api/v0/add";
        let url = reqwest::Url::parse_with_params(&base_uri, options.as_urlencode_tuple()).unwrap();
        let form =
            reqwest::multipart::Form::new().text("file", serde_json::to_string(&data).unwrap());

        let client = reqwest::Client::new();
        let res = client.post(url).multipart(form).send().await?;

        Ok(serde_json::from_str(&res.text().await?).unwrap())
    }

    async fn cat(
        &self,
        arg: String,
        offset: Option<i64>,
        length: Option<i64>,
        progess: Option<bool>,
    ) -> Result<serde_json::Value, types::error::Error> {
        let base_uri = self.uri.clone() + "/api/v0/cat";
        let mut url = reqwest::Url::parse(&base_uri).unwrap();
        url.query_pairs_mut()
            .append_pair("arg", &arg)
            .append_pair("progess", &progess.unwrap_or(true).to_string());

        if let Some(offset) = offset {
            url.query_pairs_mut()
                .append_pair("offset", &offset.to_string());
        }

        if let Some(length) = length {
            url.query_pairs_mut()
                .append_pair("length", &length.to_string());
        }

        let client = reqwest::Client::new();
        let res = client.post(url).send().await?;
        //println!("{:?}", res.text().await?);
        Ok(serde_json::from_str(&res.text().await?).unwrap())
    }

    async fn pin_rm(
        &self,
        arg: String,
        recursive: Option<bool>,
    ) -> Result<serde_json::Value, types::error::Error> {
        let base_uri = self.uri.clone() + "/api/v0/pin/rm";
        let mut url = reqwest::Url::parse(&base_uri).unwrap();
        url.query_pairs_mut()
            .append_pair("arg", &arg)
            .append_pair("recursive", &recursive.unwrap_or(true).to_string());

        let client = reqwest::Client::new();
        let res = client.post(url).send().await?;
        Ok(serde_json::from_str(&res.text().await?).unwrap())
    }
}

#[cfg(test)]
mod tests {
    use types::create::Options;

    use super::*;

    #[tokio::test]
    async fn test_ipfs_client_new() {
        let client = IPFSClient::new("http://localhost:5001".to_string());
        assert_eq!(client.uri, "http://localhost:5001");
        let item = ItemData::new(
            serde_json::Value::String("test".to_string()),
            "test".to_string(),
            "test".to_string(),
        );
        let res = client.create(item, Options::default()).await.unwrap();
        println!("{:?}", res);

        let res1 = client.cat(res.get_hash(), None, None, None).await.unwrap();
        println!("{:?}", res1.to_string());

        // Unpin the item does not delete it immediately we need to wait for the GC
        let res2 = client
            .pin_rm("/".to_string() + &res.get_hash(), None)
            .await
            .unwrap();
        println!("{:?}", res2.to_string());

        let res3 = client.cat(res.get_hash(), None, None, None).await.unwrap();
        println!("{:?}", res3.to_string());
    }
}
