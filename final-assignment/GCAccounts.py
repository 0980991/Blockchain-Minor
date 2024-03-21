import hashlib
import sqlite3

class GCAccounts():
    def __init__(self):
        self.users = []

    def login(self, username, password):
        for user in self.users:
            if user.username.lower() == username.lower():
                if user.pw_hash == self.hash_string(password):
                    return user
                break
        return None

    def hash_string(self, string):
        b_string = my_string.encode('utf-8')
        str_hash = hashlib.sha256().update(b_string).hexdigest()
        return str_hash