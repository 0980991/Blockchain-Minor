import hashlib
import DbInterface as dbi
from GCUser import GCUser

class GCAccounts():
    def __init__(self):
        self.users = []
        self.user_db = dbi.DbInterface()

    def validate_account(self, username, password):
        # Declaring our password

        # Adding the salt to password

        for user in self.users:
            if self.userExists(username):
                return user
                break
        return None

    def load_users(self):
        users = self.user_db.getAllUsers()
        for user in users:
            self.users.append(GCUser())
    def userExists(self, username):
        for user in self.users:
            if user.username.lower() == username.lower():
                return True
        return False

    def encrypt_string(self, string, salt):
        pwd = string + salt
        encrypted_pw = hashlib.md5(pwd.encode('utf-8'))
        return encrypted_pw.hexdigest()

    def hash_string(self, string):
        b_string = string.encode('utf-8')
        str_hash = hashlib.sha256()
        str_hash.update(b_string)
        str_hash.hexdigest()
        return str_hash