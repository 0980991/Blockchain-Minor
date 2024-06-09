import sqlite3
from sqlite3 import DatabaseError
import HelperFunctions as hf
import sys
import os
class DbInterface:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'data', 'Accounts.db'))

    def __init__(self):
        try:
            db = sqlite3.connect(DbInterface.DATA_FILE_PATH)
            cursor = db.cursor()

            # Create the Accounts table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Accounts(
                user_name TEXT NOT NULL,
                password TEXT NOT NULL,
                private_key TEXT NOT NULL,
                public_key TEXT NOT NULL
            );''')

            db.commit()
            db.close()
        except sqlite3.DatabaseError as e:
            print("DatabaseError: ", e)
            input("ERROR [!]: Accounts.db has been corrupted due to tampering and cannot be opened.\n"
                  "Please delete the file and restart the program.\n"
                  "If the file has not been tampered with and does not exist, make sure there is a 'data' folder in your root directory.\n"
                  "Please press enter to continue...")
            sys.exit()
        except Exception as e:
            print("An unexpected error occurred: ", e)
            input("Please press enter to continue...")
            sys.exit()

    @classmethod
    def updatePwHash(cls, user_name, pw_hash):
        db = sqlite3.connect(cls.DATA_FILE_PATH)
        cursor = db.cursor()
        cursor.execute(f'UPDATE Accounts SET password = "{pw_hash}" WHERE user_name = "{user_name}"')
        db.commit()
        db.close()

    @classmethod
    def deleteUser(cls, username):
        db = sqlite3.connect(cls.DATA_FILE_PATH)
        cursor = db.cursor()
        cursor.execute(f'DELETE FROM Accounts WHERE user_name="{username}"')
        db.commit()
        db.close()

    @classmethod
    def insertUser(cls, user):
        db = sqlite3.connect(cls.DATA_FILE_PATH)
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO Accounts (user_name, password, private_key, public_key) VALUES ("{user.username}", "{user.pw_hash}", "{user.pem_private_key}", "{user.pem_public_key}")')
        db.commit()
        db.close()

    @classmethod
    def getAllUsers(cls):
        db = sqlite3.connect(cls.DATA_FILE_PATH)
        cursor = db.cursor()
        raw_users = cursor.execute(f'SELECT * FROM Accounts').fetchall()
        db.commit()
        db.close()
        return raw_users


    @classmethod
    def formatDbRow(cls, rows, attributes):
            outputstring = (20 * '=') + '\n'
            for row in rows:
                for i, userattribute in enumerate(row):
                    outputstring += attributes[i] + ": " + str(userattribute) + '\n'
                return outputstring