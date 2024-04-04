import hashlib
import DbInterface as dbi
from GCUser import GCUser

class GCAccounts():
    def __init__(self):
        self.users = []
        self.user_db = dbi.DbInterface()
        self.loadUsers()


    # def idPublicKey(self, pem_public_key):
    #     """ Get a username from a serialized public key"""
    #     for user in self.users:
    #         if user.pem_public_key == pem_public_key:
    #             return user.username

    #     return ""

    def validateAccount(self, username, password):
        # Declaring our password

        # Adding the salt to password
        for user in self.users:
            if user.username.lower() == username.lower():
                if user.pw_hash == self.encrypt_string(password, username):
                    return user
                break
        return None

    def loadUsers(self):
        users = self.user_db.getAllUsers()
        for user in users:
            self.users.append(GCUser(user[0], user[1], user[2], user[3]))

    def userExists(self, username):
        for user in self.users:
            if user.username.lower() == username.lower():
                return True
        return False

    def encrypt_string(self, string, salt):
        pwd = string + salt
        encrypted_pw = hashlib.md5(pwd.encode('utf-8'))
        return encrypted_pw.hexdigest()

    @classmethod
    def hash_string(self, string):
        b_string = string.encode('utf-8')
        str_hash = hashlib.sha256()
        str_hash.update(b_string)
        str_hash.hexdigest()
        return str_hash