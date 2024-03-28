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
        if self.logged_in:
            self.y_N_Input("Are you sure you want Logout and Quit the application?")
        sys.exit()


    def do_explore(self, args):
        print("The Good Chain: ")
        input("Press enter to continue")

    def do_help(self, args):
        print("Help deez nuts from drying out")
        pass

    def do_login(self, args):
        if not self.logged_in:
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
                user_credentials = self.readUserInput(["Enter a username:", "Enter a password:"])
                if user_credentials == []:
                    return
                else:
                    
            return
        else:
            print("*** Unknown syntax: login")

    def do_logout(self, args):
        if self.logged_in:
            self.user = None
            self.prompt = "(guest)> "
            self.logged_in = False
            print("\n[+] Logged Out!\n")
            self.set_menu_options()
        else:
            print("*** Unknown syntax: logout")

    def do_show(self, args):
        self.print_options()

    def do_signup(self, args):
        # Your signup logic here
        if not self.logged_in:

        print("Signup function called")

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

    def readUserInput(questionList):
        user_input = []
        for i, question in enumerate(questionList):
            user_input.append(input('(Press b to go back)\n\n' + question + '\n')) ## The char escape functie zou hier aangeroepen kunnen worden
            while user_input[i] == '':
                print('This field cannot be empty')
                user_input.pop() # Removes the empty space added to list
                user_input.append(input('(Press b go back)\n\n' + question + '\n'))
            if user_input[i] == 'b':
                return []
        return user_input

    def y_N_Input(question='', default_yes=True):
            if default_yes:
                question += ' (Y/n)\n'
            else:
                question += ' (y/N)\n'
            user_input = input(question)

            while user_input not in ['Y', 'N', 'y', 'n', '']:
                user_input = input('Invalid input please enter y or n\n')

            if user_input == 'Y' or user_input == 'y' or (user_input == '' and default_yes):
                return True
            return False

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
    print(get_banner())
    app.cmdloop()
