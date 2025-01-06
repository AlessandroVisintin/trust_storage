from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import os


def generate_ec(folder=None, curve="secp256k1") :
    curve = ec.SECP256K1() if curve=="secp256k1" else ec.SECP256R1()
    private_key = ec.generate_private_key(curve, default_backend())
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    if folder:
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "prvkey.pem"), "wb") as f:
            f.write(private_pem)
        with open(os.path.join(folder, "pubkey.pem"), "wb") as f:
            f.write(public_pem)
    return private_pem, public_pem


def load_hex_key(keypath:str):
    with open(keypath, 'r') as key_file:
        return key_file.read().strip()


def pem_to_hex(keypath:str):
    with open(keypath, 'rb') as pem_file:
        prv = serialization.load_pem_private_key(
            pem_file.read(),
            password=None,
            backend=default_backend()
        )
    if not isinstance(prv, ec.EllipticCurvePrivateKey):
        raise ValueError("The key in the PEM file is not an Elliptic Curve private key")
    if prv.curve.name != 'secp256k1':
        raise ValueError("The key is not a secp256k1 curve key")
    private_value = prv.private_numbers().private_value
    private_key_bytes = private_value.to_bytes(32, byteorder='big')
    return f"0x{private_key_bytes.hex()}"