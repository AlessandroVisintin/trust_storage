use thiserror::Error;

#[derive(Debug, Error)]
pub enum Error {
    #[error("HTTP error: {0}")]
    HTTPError(#[from] reqwest::Error),

    #[error("IO error: {0}")]
    IOError(#[from] std::io::Error),
}
