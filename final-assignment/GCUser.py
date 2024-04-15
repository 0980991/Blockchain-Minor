import Signature

class GCUser:
    def __init__(self, username, pw_hash, pem_private_key=None, pem_public_key=None):
        self.username = username
        self.pw_hash = pw_hash
        # utxo format [0: pem_public key, 1: amount, 2: username]
        self.utxo = None # A list of unspend outputs, used to determine the balance of the user

        if pem_private_key is None:
            self.private_key = Signature.generatePrivateKey()
            self.pem_private_key = Signature.serializePrivateKey(self.private_key)
        else:
            self.pem_private_key = pem_private_key
            self.private_key = Signature.deserializePrivateKey(pem_private_key)

        if pem_public_key is None:
            self.public_key = Signature.generatePublicKey(self.private_key)
            self.pem_public_key = Signature.serializePublicKey(self.public_key)
        else:
            self.pem_public_key = pem_public_key
            self.public_key = Signature.deserializePublicKey(pem_public_key)

    def __str__(self):
        return f"User {username}:\n{64*'='}\n{self.pem_public_key}"