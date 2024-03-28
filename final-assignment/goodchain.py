import random as r
import os
import sys
from GCAccounts import GCAccounts
from GCUser import GCUser
from CMDWrapper import CMDWrapper
import colorama
import helper_functions as hf


class GoodChainApp():

    def __init__(self):
        super().__init__()
        CMDWrapper.__init__(self)
        self.accounts = GCAccounts()
        self.accounts.users.append(GCUser("jack", self.accounts.encrypt_string("q", "jack")))
        self.logged_in = False
        self.options = None
        self.prompt = "(guest)> "
        self.set_menu_options()
        self.start()

    def start(self):
        choice = hf.optionsMenu("Welcome to the GoodChain application.\nWhat would you like to do?\n", self.options, self.prompt)
        self.options[choice][0]()

    def exit(self):
        if self.logged_in:
            hf.yesNoInput("Are you sure you want Logout and Quit the application?")
        sys.exit()

    def explore(self):
        print("The Good Chain: ")
        input("Press enter to continue")

    def help(self):
        print("Help deez nuts from drying out")
        pass

    def login(self):
        user_credentials = hf.readUserInput(["Enter a username:", "Enter a password:"])

        if not self.logged_in:
            if len(user_credentials) > 1:
                username = user_credentials[0]
                pwd = user_credentials[1]
                user = self.accounts.validate_account(username, pwd)
                if user is not None:
                    self.user = user
                    self.prompt = f"({user.username})> "
                    self.logged_in = True
                    self.set_menu_options()
                    print("\n[+] Login Sucessful!\n")
                    return
                else:
                    print("Login Failed! You've entered an incorrect username or password.\n")
                    return
            if len(user_credentials) == 1 and user_credentials[0] != "":
                print("Login Failed! Please enter a password.\n")
            else:
                if user_credentials == []:
                    return
                else:
                    pass
            return
        else:
            print("*** Unknown syntax: login")

    def do_logout(self):
        if self.logged_in:
            self.user = None
            self.prompt = "(guest)> "
            self.logged_in = False
            print("\n[+] Logged Out!\n")
            self.set_menu_options()
        else:
            print("*** Unknown syntax: logout")

    def show(self):
        self.print_options()

    def signup(self):
        # Your signup logic here
        if not self.logged_in:
            pass
        print("Signup function called")

    def explore_blockchain(self):
        # Your explore blockchain logic here
        print("Explore the Blockchain function called")

    def set_menu_options(self):
        if self.logged_in:
            self.options = [
                [self.explore, "Explore the Blockchain"]
                [self.transfer, "Transfer Coins"]
                [self.check_balance, "Check Balance"]
                [self.transaction_pool, "Transaction Pool"]
                [self.user_transactions,"Your Pending Transactions"]
                [self.mine,"Mine a Block"]
                [self.logout,"Logout"]
                [self.exit,"Exit"]
            ]
        else:
            self.options = [
                ['Login', "Use `login` to login to your account."],
                ['Explore the Blockchain', 'Use `explore` to view the current blockchain.'],
                ['Sign Up', 'Use `signup` to create a new account.'],
                ['Exit', 'Use `exit` to quit the application.']
            ]



def get_banner():
    banners = []
    with open(".\\final-assignment\\banners.txt", 'r', encoding='utf-16le') as file:
        banners_text = file.read()
        banners = banners_text.split('\n,\n')
    return ""
    return r.choice(banners)

if __name__ == "__main__":
    app = GoodChainApp()
    app.prompt = "(guest)> "
