from setuptools import setup, find_packages

setup(
    name='blockchain_toolkit',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "py-solc-x==2.0.3",
        "ecdsa==0.19.1",
        "pycryptodome==3.23.0",
        "pytest==8.3.5",
        "PyYAML==6.0.2",
        "rlp==4.1.0"
    ]
)