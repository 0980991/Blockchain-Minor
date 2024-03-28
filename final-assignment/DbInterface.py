import sqlite3

class DbInterface:
    def __init__(self):
        db = sqlite3.connect('GoodChain.db')
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Accounts(
        user_name TEXT NOT NULL,
        password HASH NOT NULL,
        private_key HASH NOT NULL,
        public_key HASH NOT NULL
        );''')
        db.commit()
        db.close()

    @classmethod
    def deleteUser(self, username):
        db = sqlite3.connect('GoodChain.db')
        cursor = db.cursor()
        cursor.execute(f'DELETE FROM Accounts WHERE user_name="{username}"')
        db.commit()
        db.close()

    @classmethod
    def insertUser(self, user):
        db = sqlite3.connect('GoodChain.db')
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO Accounts (user_name, password, private_key, public_key) VALUES ("{user.username}", "{user.pw_hash}", "{user.private_key}", "{user.public_key}")')
        db.commit()
        db.close()

    @classmethod
    def getAllUsers(self):
        db = sqlite3.connect('GoodChain.db')
        cursor = db.cursor()
        raw_users = cursor.execute(f'SELECT * FROM Accounts').fetchall()
        db.commit()
        db.close()
        
        
        return raw_users
    # @classmethod
    # def stringifyUsers(self, fetched_users, col_names):
    #     out_str = ""
    #     for i, row in enumerate(fetched_users):
    #         print(f"{[i]}. {cell}"cell)
        
        

    @classmethod
    def formatDbRow(self, rows, attributes):
            outputstring = (20 * '=') + '\n'
            for row in rows:
                for i, userattribute in enumerate(row):
                    outputstring += attributes[i] + ": " + str(userattribute) + '\n'
                return outputstring