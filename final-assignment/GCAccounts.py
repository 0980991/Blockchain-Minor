import hashlib
import sqlite3
from GCUser import GCUser

class GCAccounts():
    def __init__(self):
        self.users = []

    def validate_account(self, username, password):
        # Declaring our password

        # Adding the salt to password

        for user in self.users:
            if user.username.lower() == username.lower():
                if user.pw_hash == self.encrypt_string(password, username):
                    return user
                break
        return None

    def load_users(self,)


    def encrypt_string(self, string, salt):
        pwd = string + salt
        hashed_pw = hashlib.md5(pwd.encode('utf-8'))
        return hashed_pw.hexdigest()


    def hash_string(self, string):
        b_string = string.encode('utf-8')
        str_hash = hashlib.sha256()
        str_hash.update(b_string)
        str_hash.hexdigest()
        return str_hash