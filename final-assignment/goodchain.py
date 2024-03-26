import random as r
import sys
from GCAccounts import GCAccounts
from GCUser import GCUser
from CMDWrapper import CMDWrapper

class GoodChainApp(CMDWrapper):

    def __init__(self):
        super().__init__()
        # self.intro = "hello"
        CMDWrapper.__init__(self)
        self.accounts = GCAccounts()
        self.accounts.users.append(GCUser("jack", self.accounts.encrypt_string("q", "jack")))
        self.options = [
            ['Login', "use `login` to login to your a6ccount."],
            ['Explore the Blockchain', 'Use `explore` to view the current blockchain.'],
            ['Sign Up', 'Use `signup` to create a new account.'],
            ['Exit', 'Use `exit` to quit the application.']
        ]
        self.logged_in = False
        for i, opt in enumerate(self.options):
            print(f"{i+1}. {opt[0]} - {opt[1]}")

    def do_exit(self, args):
        sys.exit()


    def do_explore(self, args):
        print("The Good Chain: ")
        input("Press enter to continue")

    def do_login(self, args):
        args_list = args.split(" ")
        if len(args_list) > 1:
            username = args_list[0]
            pwd = args_list[1]
            user = self.accounts.login(username, pwd)
            if user is not None:
                self.user = user
                self.prompt = f"({user.username})> "
                self.logged_in = True

        print("Login Failed")
        if len(args_list) == 1:
            print("Please enter a password.")
        else:
            print("Please enter a username and password.")
        return None

    def do_logout(self, args):
        self.user

    def get_names(self):
        func_names = super().get_names()
        if not self.logged_in:
            names.remove("do_logout")

    def explore_blockchain(self):
        # Your explore blockchain logic here
        print("Explore the Blockchain function called")


    def do_signup(self, args):
        # Your signup logic here
        print("Signup function called")

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
