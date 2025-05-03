class TrustStorageClientError(Exception):
    """Base exception for all Besu client errors."""
    pass

class BlockchainError(TrustStorageClientError):
    """Raised when there's an error communicating with the blockchain."""
    pass

class KeyPairError(TrustStorageClientError):
    """Raised when there's an error with a key."""
    pass

class TransactionError(TrustStorageClientError):
    """Raised when there's an error with a transaction."""
    pass

class TransactionTimeoutError(TransactionError):
    """Raised when a transaction times out."""
    pass

class ContractError(TrustStorageClientError):
    """Raised when a contract triggers an error."""
    pass