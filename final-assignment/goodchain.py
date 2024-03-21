import random as r
import hashlib
import sys
import curses
import GCAccounts as gca
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
        self.color_pairs = {
            "red" : 1,
            "default": 2,
            "highlight" : 3
        }
        self.logged_in = False

    def show_menu(self, stdscr):
        # Turn off cursor blinking
        curses.curs_set(0)

        # Clear screen
        stdscr.clear()

        # Turn on keypad mode
        stdscr.keypad(True)

        # Define menu options
        options = ["Login", "View", "Exit"]
        num_options = len(self.options)
        selected_option = 0

        # Loop to handle user input
        while True:
            stdscr.clear()

            # Display menu options
            for i in range(num_options):
                if i == selected_option:
                    stdscr.addstr(i + 1, 1, "-> " + options[i])
                else:
                    stdscr.addstr(i + 1, 1, "   " + options[i])

            stdscr.refresh()

            # Get user input
            key = stdscr.getch()

            # Move selection up
            if key == curses.KEY_UP:
                selected_option = (selected_option - 1) % num_options

            # Move selection down
            elif key == curses.KEY_DOWN:
                selected_option = (selected_option + 1) % num_options

            # Select option
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if selected_option == num_options - 1:
                    break  # Exit the loop if "Exit" is selected
                else:
                    stdscr.addstr(num_options + 2, 1, "You selected: " + options[selected_option])
                    stdscr.getch()  # Wait for user to acknowledge selection

        # Turn off keypad mode
        stdscr.keypad(False)

    def login(self, stdscr):
        # Your login logic here
        stdscr.addstr("Please enter your username ")
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


    def run(self, stdscr=curses.initscr()):
        # Set fg/bg color 
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, -1, -1)
        curses.curs_set(0)

        # Display the banner
        banner = self.get_banner()
        banner_lines = banner.split('\n')
        for i, line in enumerate(banner_lines):
            stdscr.addstr(i, 0, line, curses.color_pair(1))

        # Display the menu
        menu_start_line = len(banner_lines) + 1
        stdscr.addstr(menu_start_line, 0, "Choose an option:", curses.color_pair(2))
        for i, (key, option, title) in enumerate(self.opts, start=menu_start_line + 2):
            stdscr.addstr(i, 2, f"{key}. {title}", curses.color_pair(2))

        while True:
            stdscr.keypad(True)
            stdscr.refresh()
            key = stdscr.getkey()
            if key == '1':
                stdscr.clear()
                stdscr.refresh()
                self.show_menu(stdscr)


# Run the application using curses wrapper
app = GoodChain()
curses.wrapper(app.run)
