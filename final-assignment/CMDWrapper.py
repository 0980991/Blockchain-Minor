import cmd
import sys
class CMDWrapper(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.help_intro: str
        # The CMD module contains a bug that is introduced after python 3.11 which prevents the autocomplete from working. Below is a workaround
        # https://github.com/python/cpython/issues/102130
        # if 'libedit' in readline.__doc__:
        #     # Found libedit readline
        #     readline.parse_and_bind("bind ^I rl_complete")
        # else:
        #     # Found GNU readline
        #     readline.parse_and_bind("tab: complete")

    def do_exit(self, arg):
        sys.exit()

    def do_1(self, arg):
        print("Function: 1")

    def do_2(self, arg):
        print("Function: 2")