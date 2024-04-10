from cryptography.exceptions import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def generatePrivateKey():
    return rsa.generate_private_key(public_exponent=65537,key_size=2048)

def generatePublicKey(private_key):
    return private_key.public_key()

def serializePrivateKey(private_key):
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

def serializePublicKey(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserializePrivateKey(pem_private_key):
    return serialization.load_pem_private_key(pem_private_key, password=None, backend=default_backend())

def deserializePublicKey(pem_public_key):
    return serialization.load_pem_public_key(pem_public_key, backend=default_backend())

def sign(message, private_key):
    message = bytes(str(message), 'utf-8')
    signature = private_key.sign(
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
        )
    # print(f"Message:\n{message}\n\nsig:\n{signature}")
    return signature

def verify(message, signature, public_key):
    message = bytes(str(message), 'utf-8')
    # print(f"Message:\n{message}\n\nsig:\n{signature}")

    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
            )
        return True
    except InvalidSignature:
         return False
    # except:
    #     print('Error executing public_key.verify')
    #     return False