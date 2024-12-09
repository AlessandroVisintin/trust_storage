use josekit::{jws::ES256, jwt};

pub mod payload;
use payload::Payload;

pub fn verify(jwt: String, public_key: String) -> Result<Payload, String> {
    let verifier = ES256.verifier_from_pem(&public_key).unwrap();
    match jwt::decode_with_verifier(&jwt, &verifier) {
        Ok((payload, _header)) => {
            let data: Payload = serde_json::from_str(format!("{}", payload).as_str()).unwrap();
            //if data.is_expired() {
            //    return Err("Token is expired".to_string());
            //}
            Ok(data)
        }
        Err(error) => Err(error.to_string()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use josekit::jws::JwsHeader;
    use josekit::jwt::JwtPayload;
    use std::time::{Duration, SystemTime};

    const PRIVATE_KEY: &str = concat!(env!("CARGO_MANIFEST_DIR"), "/configs/ec.key");
    const PUBLIC_KEY: &str = concat!(env!("CARGO_MANIFEST_DIR"), "/configs/ec.pub");

    pub fn sign(
        tbom: Option<serde_json::Value>,
        validity_time: Option<u64>,
    ) -> Result<String, Box<dyn std::error::Error>> {
        let mut header = JwsHeader::new();
        header.set_token_type("JWT");

        let mut payload = JwtPayload::new();
        payload.set_subject("gatekeeper");
        payload.set_issuer("rescale");
        payload.set_issued_at(&SystemTime::now());
        let expires = SystemTime::now() + Duration::from_secs(validity_time.unwrap_or(60));
        payload.set_expires_at(&expires);
        let _ = payload.set_claim("tbom", tbom);

        // Signing JWT
        let private_key = std::fs::read(PRIVATE_KEY)?;
        let signer = ES256.signer_from_pem(&private_key)?;
        Ok(jwt::encode_with_signer(&payload, &header, &signer)?)
    }

    #[test]
    fn test_sign_and_verify() {
        let tbom = serde_json::json!({
            "tbom": "test",
        });
        let token = sign(Some(tbom), Some(60000)).unwrap();
        println!("{}", token);
        assert_eq!(token.is_empty(), false);

        let public_key = std::fs::read_to_string(PUBLIC_KEY).unwrap();
        let payload = verify(token, public_key).unwrap();
        println!("{:?}", payload);
    }

    #[test]
    fn verify_expired_token() {
        let tbom = serde_json::json!({
            "tbom": "test",
        });
        let token = sign(Some(tbom), Some(0)).unwrap();
        println!("{}", token);
        assert_eq!(token.is_empty(), false);

        std::thread::sleep(Duration::from_secs(5));

        let public_key = std::fs::read_to_string(PUBLIC_KEY).unwrap();
        let res = verify(token, public_key);
        assert_eq!(res.is_err(), true);
        assert_eq!(res.unwrap_err(), "Token is expired");
    }
}
