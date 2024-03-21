#!/usr/bin/env python3
"""Asymmetric Cryptography -> Digital Signature: Homework

The goal of this homework is to learn how to store and load asymmetric keys of different users on a disk.
In addition, to sign and verify messages using those keys. Furthermore, it is required to encrypt keys before saving using a password.
In this implementation the passed message as an argument is a string. Proper encoding and decoding is need before usage.
When signing a message the RSA sign-function requires a specific hash like SHA256, and padding such as PSS.
RSA verify function calculates the message hash. Decrypt the signature then compares both values to verify.
Be aware that verification must use the same algorithm values as signing to correctly verify the signature.

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code
    * run the test of this tutorial located in same folder.

To test run 'Signature_t.py' in your command line

Notes:
    * do not change class structure or method signature to not break unit tests
    * visit this url for more information on this topic:
    https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
"""

from cryptography.exceptions import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat


def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

# TODO 1: Sign a passed message using a given private key
# Make sure the message is encoded correctly before signing
# Signing and verifying algorithms must be the same
def sign(message, private_key):
    b_msg = message.encode('utf-8')
    signature = private_key.sign(
        b_msg,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


# TODO 2: Verify a signature for a message using a given public key
# Make sure the message is decoded correctly before verifying
# Signing and verifying algorithms values must be the same
def verify(message, signature, public_key):
    b_msg = message.encode('utf-8')
    try:
        public_key.verify(
            signature,
            b_msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

# TODO 3: Store the list of keys into a given file.
# In this implementation passwords are used for additional security
# Make sure of proper PEM encoding before serialization
def save_keys(keys_file_name, keys, pw):
    prv_key, pbc_key = keys
    b_pw = pw.encode('utf-8')
    prv_key_pem = prv_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(b_pw), # You can use a password for encryption if needed
    )
    pbc_key_pem = pbc_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(f"{keys_file_name}.pem", "wb") as f:
        f.write(prv_key_pem)
        f.write(pbc_key_pem)

# TODO 4: Load asymmetric keys from a given file and return those keys as a tuple
# In this implementation passwords are used for additional security
# Make sure of proper PEM decoding when deserializing
def load_keys(keys_file_name, pw):
    b_pw = pw.encode('utf-8')
    with open(f"{keys_file_name}.pem", "rb") as key_file:
        pem_data = key_file.read()
        pem_prv_key, pem_pbc_key = pem_data.split(b'-----BEGIN PUBLIC KEY-----')
        pem_pbc_key = b'-----BEGIN PUBLIC KEY-----' + pem_pbc_key
        prv_key = serialization.load_pem_private_key(
            pem_prv_key,
            password=b_pw,
        )
        pbc_key = serialization.load_pem_public_key(
            pem_pbc_key,

        )
    return prv_key, pbc_key