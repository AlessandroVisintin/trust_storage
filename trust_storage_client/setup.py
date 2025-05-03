from setuptools import setup, find_packages

setup(
    name='trust_storage_client',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "cryptography==43.0.3",
        "eth-abi==5.1.0",
        "eth-account==0.13.4",
        "PyJWT==2.10.0",
        "requests==2.32.3",
        "web3==7.5.0",
        "pytest==8.3.5",
        "pytest-mock==3.14.0"
    ]
)