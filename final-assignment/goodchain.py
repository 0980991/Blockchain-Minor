import random as r
import CMDWrapper as cmdw
banners = [
r"""
   __|                  |   __|  |           _)
  (_ |   _ \   _ \   _` |  (       \    _` |  |    \
 \___| \___/ \___/ \__,_| \___| _| _| \__,_| _| _| _|
 developed by Maurice Monster
"""
]

class GoodChain(cmdw.CMDWrapper):
    def __init__(self):
        cmdw.CMDWrapper.__init__(self)
        self.opts = ['1. Login (`login`)',
                     '2. Explore the Blockchain',
                     '3. Signup',
                     '4. Exit']
        self.help_intro = f"\nWelcome to the GoodChain:\n- {self.opts}\n<Print-Options-Here>"

   def do_login(self):

app = GoodChain()
app.prompt = ">> "
version_nr = "v1.0" # TODO: Add username when user is logged in
banner = r.choice(banners) + "\n" + version_nr
app.cmdloop(banner)