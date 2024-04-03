import Signature

class GCUser:
    def __init__(self, username, pw_hash, private_key=None, public_key=None):
        self.username = username
        self.pw_hash = pw_hash
        # Get Public Key
        if private_key is None:
            self.private_key, self.public_key = Signature.generateKeys()
        else:
            self.private_key = private_key
        # Get Private Key
        if public_key is None:
            self.pem_private_key, self.pem_public_key = Signature.serializeKeys(self.private_key, self.public_key)
        else:
            self.public_key = public_key

    def __str__(self):
        return f"User {username}:\n{20*'='}\n{self.pem_public_key}"