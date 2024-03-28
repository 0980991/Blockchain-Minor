import random as r
import os
import sys
from GCAccounts import GCAccounts
from GCUser import GCUser
import colorama
from helper_functions import HelperFunctions
from DbInterface import DbInterface as dbi


class GoodChainApp():

    def __init__(self):
        self.hf = HelperFunctions()
        self.accounts = GCAccounts()
        self.logged_in = False
        self.options = None
        self.set_menu_options()

    def start(self):
        while True:
            choice = self.hf.optionsMenu("Welcome to the GoodChain application.\nWhat would you like to do?", self.options)
            self.options[choice][0]()


    def exit(self):
        if self.logged_in:
            if self.hf.yesNoInput("Are you sure you want Logout and Quit the application?"):
                sys.exit()

    def explore(self):
        print("The Good Chain: ")
        self.hf.enterToContinue("")

    def help(self):
        print("Help deez nuts from drying out")
        pass

    def login(self):
        user_credentials = self.hf.readUserInput(["Enter your username:", "Enter your password:"])
        if user_credentials == []:
            return
        try_again = True
        while try_again:
            if not self.logged_in:
                username = user_credentials[0]
                pwd = user_credentials[1]
                user = self.accounts.validate_account(username, pwd)
                if user is not None:
                    self.user = user
                    self.hf.prompt = f"({user.username})> "
                    self.logged_in = True
                    self.set_menu_options()
                    self.hf.enterToContinue("\n[+] Login Sucessful!\n")
                    return
                else:
                    if self.hf.yesNoInput("Login Failed! You've entered an incorrect username or password.\nDo you want to try again?"):
                        user_credentials = self.hf.readUserInput(["Enter your username:", "Enter your password:"])
                        if user_credentials == []:
                            return
                    else:
                        try_again = False
    def sign_up(self):
        user_credentials = self.hf.readUserInput(["Enter a username:", "Enter a password:"])
        # Check if user exits!
        username = user_credentials[0]
        if not self.accounts.user_exists(username):
            hashed_pw = self.accounts.hash_string(user_credentials[1])
            new_user = GCUser(username, hashed_pw)
            self.accounts.users.append(GCUser(user_credentials[0], user_credentials[1]))
            dbi.insertUser(new_user)
            if self.hf.yesNoInput("\n[+] Login Sucessful!\nDo you want to login now?"):
                self.login()
        else:
            self.hf.enterToContinue("This username has already been taken!")

    def explore_blockchain(self):
        # Your explore blockchain logic here
        print("Explore the Blockchain function called")

    def set_menu_options(self):
        if self.logged_in:
            self.options = [
                [self.explore, "Explore the Blockchain"],
                [self.transfer, "Transfer Coins"],
                [self.check_balance, "Check Balance"],
                [self.transaction_pool, "Transaction Pool"],
                [self.user_transactions, "Your Pending Transactions"],
                [self.mine, "Mine a Block"],
                [self.logout, "Logout"],
                [self.exit, "Exit"],
            ]
        else:
            self.options = [
                [self.login, "Login"],
                [self.explore, "Explore the Blockchain"],
                [self.sign_up, "Sign Up"],
                [self.exit,"Exit"]
            ]
    def logout(self):
        if self.logged_in:
            self.user = None
            # self.hf.prompt = "(guest)> "
            self.logged_in = False
            print("\n[+] Logged Out!\n")
            self.set_menu_options()
        else:
            print("*** Unknown syntax: logout")

    def transfer(self):
        pass
    def check_balance(self):
        pass
    def transaction_pool(self):
        pass
    def user_transactions(self):
        pass
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