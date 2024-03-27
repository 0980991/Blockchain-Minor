import random as r
import os
import sys
from GCAccounts import GCAccounts
from GCUser import GCUser
from CMDWrapper import CMDWrapper
import colorama


class GoodChainApp(CMDWrapper):

    def __init__(self):
        super().__init__()
        CMDWrapper.__init__(self)
        self.accounts = GCAccounts()
        self.accounts.users.append(GCUser("jack", self.accounts.encrypt_string("q", "jack")))
        self.logged_in = False
        self.options = None
        self.set_menu_options()
        self.print_options()


    def do_exit(self, args):
        sys.exit()


    def do_explore(self, args):
        print("The Good Chain: ")
        input("Press enter to continue")

    def do_help(self, args):
        print("Help deez nuts from drying out")
        pass

    def do_login(self, args):
        args_list = args.split(" ")
        if len(args_list) > 1:
            username = args_list[0]
            pwd = args_list[1]
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
        if len(args_list) == 1 and args_list[0] != "":
            print("Login Failed! Please enter a password.\n")
        else:
            print("Login Failed! Please enter a username and password.\n")
        return

    def do_logout(self, args):
        self.user = None
        self.prompt = "(guest)> "
        self.logged_in = False
        print("\n[+] Logged Out!\n")
        self.set_menu_options()


    def do_show(self, args):
        self.print_options()

    def do_signup(self, args):
        # Your signup logic here
        
        print("Signup function called")

    def get_names(self):
        func_names = super().get_names()
        if self.logged_in:
            names.remove("do_login")
            names.remove("do_signup")
        if not self.logged_in:
            names.remove("do_logout")
            names.remove

    def explore_blockchain(self):
        # Your explore blockchain logic here
        print("Explore the Blockchain function called")

    def print_options(self,):
        for i, opt in enumerate(self.options):
            print(f"{i+1}. {opt[0]} - {opt[1]}")

    def set_menu_options(self):
        if self.logged_in:
            self.options = [
                ['Explore the Blockchain', 'Use `explore` to view the current blockchain.'],
                ["Transfer Coins", "Use `transfer` to transfer your coins to an address."],
                ["Check Balance", "Use `balance` to view your current balance."],
                ["Transaction Pool", "Use `pool` to view the current transaction pool"],
                ["Your Pending Transactions", "Use `pending` to manage your current pending transactions."],
                ["Mine a Block", "Use `mine` to mine a new block."],
                ["Logout", "Use `logout` to logout of the application"],
                ["Exit", "Use `exit` to logout and quit the application."]
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
    with open(".\\banners.txt", 'r', encoding='utf-16le') as file:
        banners_text = file.read()
        banners = banners_text.split('\n,\n')
    return ""
    return r.choice(banners)

if __name__ == "__main__":
    app = GoodChainApp()
    app.prompt = "(guest)> "
    print(get_banner())
    app.cmdloop()
