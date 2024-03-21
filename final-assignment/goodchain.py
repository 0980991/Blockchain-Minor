import random as r
# import CMDWrapper as cmdw
import hashlib
import sys
import curses
# import GCAccounts as gca
import curses
import random

class GoodChain:
    def __init__(self):
        self.opts = [
            ['1', self.login, 'Login'],
            ['2', self.explore_blockchain, 'Explore the Blockchain'],
            ['3', self.signup, 'Sign Up'],
            ['4', self.exit, 'Exit']
        ]
        self.selected_option = '1'  # Initially select the first option

    def login(self):
        # Your login logic here
        print("Login function called")

    def explore_blockchain(self):
        # Your explore blockchain logic here
        print("Explore the Blockchain function called")

    def signup(self):
        # Your signup logic here
        print("Signup function called")

    def exit(self):
        sys.exit()

    def load_banners(self):
        banners = []
        with open("banners.txt", 'r', encoding='utf-16le') as file:
            banners_text = file.read()
            print("HELLLLO")
            banners = banners_text.split('\n,\n')
        return banners

    def run(self, stdscr):
        # Set fg/bg color 
        # curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.curs_set(0)

        # Display the banner
        banner = random.choice(self.load_banners())
        banner_lines = banner.split('\n')
        for i, line in enumerate(banner_lines):
            stdscr.addstr(i, 0, line, curses.color_pair(2))

        # Display the menu
        menu_start_line = len(banner_lines) + 1
        stdscr.addstr(menu_start_line, 0, "Choose an option:", curses.color_pair(1))
        for i, (key, option, title) in enumerate(self.opts, start=menu_start_line + 2):
            stdscr.addstr(i, 2, f"{key}. {title}", curses.color_pair(1))

        while True:
            stdscr.refresh()
            key = stdscr.getkey()


# Run the application using curses wrapper
app = GoodChain()
curses.wrapper(app.run)
print("hellox")

