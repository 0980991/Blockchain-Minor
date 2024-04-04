import random as r
import os
import sys
from GCAccounts import GCAccounts
from GCUser import GCUser
import colorama
from helper_functions import HelperFunctions
from DbInterface import DbInterface as dbi
from GCTx import GCTx
from TxPool import TxPool


class GoodChainApp():

    def __init__(self):
        self.hf = HelperFunctions()
        self.accounts = GCAccounts()
        self.tx_pool = TxPool()
        self.tx_pool.load()
        self.logged_in = False
        self.user = None
        self.options = None
        self.setMenuOptions()

    def start(self):
        while True:
            choice = self.hf.optionsMenu("Welcome to the GoodChain application.\nWhat would you like to do?", self.options)
            self.options[choice][0]()

    def exit(self):
        if self.logged_in:
            if self.hf.yesNoInput("Are you sure you want Logout and Quit the application?"):
                sys.exit()
            return
        sys.exit()

    def explore(self):
        print("The Good Chain: ")
        self.hf.enterToContinue("")

    def login(self):
        user_credentials = self.hf.readUserInput(["Enter your username:", "Enter your password:"])
        if user_credentials == []:
            return
        try_again = True
        while try_again:
            if not self.logged_in:
                username = user_credentials[0]
                pwd = user_credentials[1]
                user = self.accounts.validateAccount(username, pwd)
                if user is not None:
                    self.user = user
                    self.hf.prompt = f"({user.username})> "
                    self.logged_in = True
                    self.setMenuOptions()
                    self.hf.enterToContinue("\n[+] Login Sucessful!\n")
                    return
                else:
                    if self.hf.yesNoInput("Login Failed! You've entered an incorrect username or password.\nDo you want to try again?"):
                        user_credentials = self.hf.readUserInput(["Enter your username:", "Enter your password:"])
                        if user_credentials == []:
                            return
                    else:
                        try_again = False

    def logout(self):

        self.user = None
        self.hf.prompt = "(guest)> "
        self.logged_in = False
        print("\n[+] Logged Out!\n")
        self.setMenuOptions()


    def signUp(self):
        user_credentials = self.hf.readUserInput(["Enter a username:", "Enter a password:"])
        if user_credentials == []:
            input("Login canceled!")
            return
        username = user_credentials[0]
        if not self.accounts.userExists(username):
            hashed_pw = self.accounts.hash_string(user_credentials[1])
            new_user = GCUser(username, hashed_pw)
            self.accounts.users.append(new_user)

            dbi.insertUser(new_user)

            self.tx_pool.add(GCTx([("REWARD", 50)], [(new_user.pem_public_key, 50)]))

            if self.hf.yesNoInput("\n[+] Login Sucessful!\nDo you want to login now?"):
                self.login()
        else:
            self.hf.enterToContinue("This username has already been taken!")

    def setMenuOptions(self):
        if self.logged_in:
            self.options = [
                [self.explore, "Explore the Blockchain"],
                [self.transfer, "Transfer Coins"],
                [self.checkBalance, "Check Balance"],
                [self.viewTransactionPool, "Transaction Pool"],
                [self.userTransactions, "Your Pending Transactions"],
                [self.mine, "Mine a Block"],
                [self.logout, "Logout"],
                [self.exit, "Exit"],
            ]
        else:
            self.options = [
                [self.login, "Login"],
                [self.explore, "Explore the Blockchain"],
                [self.signUp, "Sign Up"],
                [self.exit,"Exit"]
            ]

    def transfer(self):
        amount,self.hf.readUserInput(["Enter the username or wallet address of the receiver", "Please enter the amount you would like to transfer"])

    def checkBalance(self):
        pass

    def viewTransactionPool(self):
        print(self.tx_pool)

    def userTransactions(self):
        user_transactions = self.tx_pool.getUserTransactions(self.user.public_key)

    def mine(self):
        pass

def get_banner():
    banners = []
    with open(".\\banners.txt", 'r', encoding='utf-16le') as file:
        banners_text = file.read()
        banners = banners_text.split('\n,\n')
    return r.choice(banners)

if __name__ == "__main__":
    app = GoodChainApp()
    app.start()
