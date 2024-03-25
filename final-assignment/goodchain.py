import random as r
import sys
import GCAccounts as gca
from time import monotonic
from textual.app import App, ComposeResult
from textual.containers import *
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static

class GoodChainApp(App):
    CSS_PATH = "goodchain.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle Dark Mode")
        # TODO Add Shortcuts login, signup, explore and exit
    ]
    
    def __init__(self):
        super().__init__()
        self.opts = [
            [self.login, 'Login'],
            [self.explore_blockchain, 'Explore the Blockchain'],
            [self.signup, 'Sign Up'],
            [self.exit, 'Exit']
        ]
        self.logged_in = False

    def compose(self):
        yield Header()
        yield Footer()
        yield Container(Button("Login", id="login"), Button("Explore the Blockchain", id="explore"), Button("Sign up", id="signup"), Button("Exit", id="exit_btn"), id="menu")

    def on_button_pressed(self, event):
        button_id = event.button.id
        if button_id == "exit":
            sys.exit()
            self.exit()
        

    def get_user_input(self, prompt=""):
        pass

    def login(self):
        # Your login logic here
        print("Login func called")

    def explore_blockchain(self):
        # Your explore blockchain logic here
        print("Explore the Blockchain function called")

    def signup(self):
        # Your signup logic here
        print("Signup function called")

    def exit(self):
        sys.exit()

    def get_banner(self):
        banners = []
        with open("banners.txt", 'r', encoding='utf-16le') as file:
            banners_text = file.read()
            banners = banners_text.split('\n,\n')
        return random.choice(banners)

if __name__ == "__main__":
    app = GoodChainApp()
    app.run()
