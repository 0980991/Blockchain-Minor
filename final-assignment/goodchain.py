import random as r
import os
import sys
from GCAccounts import GCAccounts
from GCUser import GCUser
from GCBlock import GCBlock
from helper_functions import HelperFunctions
from DbInterface import DbInterface as dbi
from GCTx import GCTx
from TxPool import TxPool
from BlockChain import BlockChain

class GoodChainApp():

    def __init__(self):
        self.hf = HelperFunctions()
        self.accounts = GCAccounts()
        self.tx_pool = TxPool()
        self.tx_pool.load()
        self.blockchain = BlockChain()
        self.logged_in = False
        self.user = None
        self.options = None
        self.setMenuOptions()

    def test(self):
        prev_block = self.blockchain.getPrevBlock()
        new_block =GCBlock(self.tx_pool.getTxData(), prev_block)
        new_block.mine()
        self.blockchain.add(new_block)
        self.blockchain.save()

    def start(self):
        while True:
            self.test()
            choice = self.hf.optionsMenu("Welcome to the GoodChain application.\nWhat would you like to do?", self.options)
            self.options[choice][0]()


    def exit(self):
        if self.logged_in:
            if self.hf.yesNoInput("Are you sure you want Logout and Quit the application?"):
                sys.exit()
            return
        sys.exit()

    def explore(self):
        print("The Good Chain: ")
        self.hf.enterToContinue("")

    def login(self):
        user_credentials = self.hf.readUserInput(["Enter your username:", "Enter your password:"])
        if user_credentials == []:
            return
        try_again = True
        while try_again:
            if not self.logged_in:
                username = user_credentials[0]
                pwd = user_credentials[1]
                pw_hash = self.accounts.hash_string(user_credentials[1])

                user = self.accounts.validateAccount(username, pw_hash)
                if user is not None:
                    self.user = user
                    self.hf.prompt = f"({user.username})> "
                    self.logged_in = True
                    self.setMenuOptions()
                    self.hf.enterToContinue("\n[+] Login Sucessful!\n")
                    return
                else:
                    if self.hf.yesNoInput("Login Failed! You've entered an incorrect username or password.\nDo you want to try again?"):
                        user_credentials = self.hf.readUserInput(["Enter your username:", "Enter your password:"])
                        if user_credentials == []:
                            return
                    else:
                        try_again = False

    def logout(self):
        self.user = None
        self.hf.prompt = "(guest)> "
        self.logged_in = False
        print("\n[+] Logged Out!\n")
        self.setMenuOptions()

    def signUp(self):
        user_credentials = self.hf.readUserInput(["Enter a username:", "Enter a password:"])
        if user_credentials == []:
            input("Login canceled!")
            return
        username = user_credentials[0]
        if not self.accounts.userExists(username):
            hashed_pw = self.accounts.hash_string(user_credentials[1])
            new_user = GCUser(username, hashed_pw)
            self.accounts.users.append(new_user)

            dbi.insertUser(new_user)
            tx_reward = GCTx()
            self.tx_pool.add([("REWARD", 50)], [(new_user.pem_public_key, 50)])

            if self.hf.yesNoInput("\n[+] Signup Successful!\nDo you want to login now?"):
                self.login()
        else:
            self.hf.enterToContinue("This username has already been taken!")

    def setMenuOptions(self):
        if self.logged_in:
            self.options = [
                [self.explore, "Explore the Blockchain"],
                [self.transfer, "Transfer Coins ✓ (validation)"],
                [self.checkBalance, "Check Balance"],
                [self.viewTransactionPool, "View Transaction Pool ✓"],
                [self.userTransactions, "Your Pending Transactions ✓"],
                [self.mineBlock, "Mine a Block"],
                [self.viewAccountDetails, "View Your Account Details (private & public key)"],
                [self.logout, "Logout"],
                [self.exit, "Exit"],
            ]
        else:
            self.options = [
                [self.login, "Login"],
                [self.explore, "Explore the Blockchain"],
                [self.signUp, "Sign Up"],
                [self.exit,"Exit"]
            ]

    def transfer(self):
        valid_input = False
        while not valid_input:
            try:
                username, amount, gas_fee = self.hf.readUserInput(["Enter the username of the receiver", "Please enter the amount you would like to transfer", "Please enter the gas fee amount."])
                valid_input=True
            except ValueError:
                # User canceled and the function returned an empty list.
                return

        # Use if send_amount.isdigit()
        send_amount = int(amount)
        gas_fee = int(gas_fee)
        receive_amount = send_amount - gas_fee
        if gas_fee >= 0 and gas_fee < send_amount:
            if self.user.username != username and self.accounts.userExists(username):
                # TODO Have verification prompt if found, else 'user not found'
            
                tx = GCTx([(self.user.username, send_amount)], [(username, receive_amount)], gas_fee)
                tx.sign(self.user.private_key)
                self.tx_pool.add(tx)
            else:
                self.hf.enterToContinue("ERROR: User not found")
            # TODO Validate the receiver is not the user
        else:
            self.hf.enterToContinue(f"ERROR: The gas fee must be between 0 and {send_amount}.")

    def checkBalance(self):
        pass

    def viewTransactionPool(self):
        print(self.tx_pool)
        self.hf.enterToContinue()

    def userTransactions(self):
        user_transactions = self.tx_pool.getUserTransactions(self.user.username)
        print(user_transactions)
        tx_id = self.hf.readUserInput2()
        if tx_id == 'b':
            return
        else:
            self.tx_pool.remove(tx_id)
        self.hf.enterToContinue()

    def mineBlock(self):
        # Check if there 5 tx in transaction pool
        if len(self.tx_pool.transactions) < 5:
            self.hf.enterToContinue(f"There are currently {len(self.tx_pool.transactions)} in the transaction pool but at least 5 are required to create block.")
            return
        
        prev_block = self.blockchain.getPrevBlock()
        new_block =GCBlock(self.tx_pool.getTxData(), prev_block)
        new_block.mine()
        self.blockchain.add(new_block)
        self.blockchain.save()
        pass

    def viewAccountDetails(self):
        print(f"{64*'='}\nUsername: {self.user.username}:\n{64*'-'}\nPublic Key:\n{self.user.pem_public_key.decode('utf-8')}\n{self.user.pem_private_key.decode('utf-8')}\n")
        self.hf.enterToContinue()


def get_banner():
    banners = []
    with open(".\\banners.txt", 'r', encoding='utf-16le') as file:
        banners_text = file.read()
        banners = banners_text.split('\n,\n')
    return r.choice(banners)

if __name__ == "__main__":
    app = GoodChainApp()
    app.start()
