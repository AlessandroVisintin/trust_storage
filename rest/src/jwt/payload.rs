use std::time::SystemTime;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct Payload {
    sub: String,
    iss: String,
    iat: u32,
    exp: u32,
    tbom: Option<serde_json::Value>,
}

impl Payload {
    pub fn _is_expired(&self) -> bool {
        self.exp
            < SystemTime::now()
                .duration_since(SystemTime::UNIX_EPOCH)
                .unwrap()
                .as_secs() as u32
    }

    pub fn get_tbom(&self) -> Option<serde_json::Value> {
        self.tbom.clone()
    }
}

impl std::fmt::Display for Payload {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(
            f,
            "sub: {}, iss: {}, iat: {}, exp: {}, tbom: {:?}",
            self.sub, self.iss, self.iat, self.exp, self.tbom
        )
    }
}
