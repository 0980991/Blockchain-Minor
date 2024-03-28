import Signature

class GCUser:
    def __init__(self, username, pw_hash, prv_key=None, pbc_key=None):
        self.username = username
        self.pw_hash = pw_hash
        # Get Public Key
        if prv_key is None:
            self.private_key, self.public_key = Signature.generate_keys()
        else:
            self.private_key = prv_key
        # Get Private Key
        if pbc_key is None:
            self.pem_private_key, self.pem_public_key = Signature.serialize_keys(self.private_key, self.public_key)
        else:
            self.public_key = pbc_key

    def __str__(self):
        return f"User {username}:\n{20*'='}\n{self.pem_public_key}"