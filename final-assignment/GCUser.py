import Signature

class GCUser:
    def __init__(self, username, pw_hash):
        self.username = username
        self.pw_hash = pw_hash
        self.private_key, self.public_key = Signature.generate_keys()
        self.pem_private_key, self.pem_public_key = Signature.serialize_keys(self.private_key, self.public_key)

    def __str__(self):
        return f"User {username}:\n{20*'='}\n{self.pem_public_key}"