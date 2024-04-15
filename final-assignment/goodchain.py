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
import time

## QUESTIONS:
# 1. Does genesis block have to be mined? Does it need a hash of 000

class GoodChainApp():

    def __init__(self):
        self.hf = HelperFunctions()
        self.accounts = GCAccounts()
        self.tx_pool = TxPool()
        self.tx_pool.load()
        self.tx_pool.sort()
        self.blockchain = BlockChain()
        self.logged_in = False
        self.user = None
        self.options = None
        self.setMenuOptions()

    def test(self):

        self.user = self.accounts.users[0]
        self.user.utxo = self.blockchain.calculateUTXO(self.user.username)
        ## TEST EXPLORE
        # self.explore()
        # TEST MINING
        # new_hashes = []
        # for i in range(20):
        #     start_time = time.time()
        #     prev_block = self.blockchain.getPrevBlock()
        #     new_block =GCBlock(self.tx_pool.getTxData(), prev_block)
        #     new_block.mine()
        #     self.blockchain.add(new_block)
        #     self.blockchain.save()
        #     end_time = time.time()  # Record the end time
        #     duration = end_time - start_time
        #     new_hashes.append([self.blockchain.chain[-1].blockHash, duration])
        #     # self.hf.enterToContinue(f"Block sucesfully mined in {duration} seconds! Hash = {self.blockchain.chain[-1].blockHash}")
        # for i, hasht in enumerate(new_hashes):
        #     print(f"[{i+1}] {hasht[1]}  seconds")
        self.hf.enterToContinue()
        pass


    def start(self):
        # self.test()
        while True:
            choice = self.hf.optionsMenu("Welcome to the GoodChain application.\nWhat would you like to do?", self.options)
            self.options[choice][0]()


    def exit(self):
        if self.logged_in:
            if self.hf.yesNoInput("Are you sure you want Logout and Quit the application?"):
                sys.exit()
            return
        sys.exit()

    def explore(self):
        self.hf.enterToContinue(str(self.blockchain))

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
                    self.user.utxo = self.blockchain.calculateUTXO(self.user.pem_public_key)
                    # self.calculateUTXO()
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


    def calculateUTXO(self):
        # Scan blockchain
        for block in self.blockchain.chain:
            for transaction in block.transactions:
                for output in transaction.outputs:
                    if self.user.username in self.accounts.users:
                        self.accounts.users[self.user.username].add_utxo(output)

                for inp in transaction.inputs:
                    if inp.spends_utxo:
                        spender = inp.spender
                        if spender in self.accounts.users:
                            self.accounts.users[spender].remove_utxo(input.spends_utxo)

        # Calculate balances
        for username, user in self.accounts.users.items():
            balance = sum(utxo.amount for utxo in user.utxos)
            user.balance = balance

        # Update database with recalculated balances
        update_database_with_user_data(self.accounts.users)

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

            tx_reward = GCTx([("REWARD", 50, "Signup Reward")], [(new_user.pem_public_key, 50, new_user.username)])
            self.tx_pool.add(tx_reward)

            if self.hf.yesNoInput("\n[+] Signup Successful!\nDo you want to login now?"):
                self.login()
        else:
            self.hf.enterToContinue("This username has already been taken!")

    def setMenuOptions(self):
        if self.logged_in:
            self.options = [
                [self.explore, "Explore the Blockchain ✓"],
                [self.transfer, "Transfer Coins (Still requires validation)"],
                [self.checkBalance, "Check Balance"],
                [self.viewTransactionPool, "View Transaction Pool ✓"],
                [self.userTransactions, "Your Pending Transactions ✓"],
                [self.mineBlock, "Mine a Block"],
                [self.viewAccountDetails, "View Your Account Details (private & public key)"],
                [self.logout, "Logout"],
                [self.exit, "Exit"],
                [self.addTransactionsDebug, "Add Tx (DEBUG)"]
            ]
        else:
            self.options = [
                [self.login, "Login"],
                [self.explore, "Explore the Blockchain"],
                [self.signUp, "Sign Up"],
                [self.exit,"Exit"]
            ]

    def addTransactionsDebug(self):
        for i in range(5):
            tx_reward = GCTx([("REWARD", 50, "Signup Reward")], [(self.user.pem_public_key, 50, self.user.username)])
            self.tx_pool.add(tx_reward)
            # while username == self.user.username:
            #     username = r.choice(["joe", "mark", "q", "ari"])
            # send_amount = r.choice([20, 40, 50, 1000, 100])
            # gas_fee = r.choice([1,2,4,8,16])
            # receive_amount = send_amount - gas_fee
            # ins = [(self.user.pem_public_key, send_amount, self.user.username)]
            # utxo_amount = 0
            # outs = [(self.accounts.publicKeyFromUsername(username), receive_amount, username), (self.user.pem_public_key, utxo_amount, self.user.username)]
            # tx = GCTx(ins, outs, gas_fee)
            # tx.sign(self.user.private_key)
            # self.tx_pool.add(tx)

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

                utxo_sum = 0
                utxo_i = 0
                while utxo_sum < send_amount:
                    utxo_sum += self.user.utxo[utxo_i][1]
                    utxo_i += 1
                sender_change = utxo_sum - send_amount

                if sender_change > 0:
                    # Add Sender change output
                    tx = GCTx([(self.user.pem_public_key, utxo_sum, self.user.username)],
                            [(self.accounts.publicKeyFromUsername(username), receive_amount, username), (self.user.pem_public_key,sender_change, self.user.username)],
                            gas_fee)
                else:
                    tx = GCTx([(self.user.pem_public_key, send_amount, self.user.username)],
                            [(self.accounts.publicKeyFromUsername(username), receive_amount, username)],
                            gas_fee)

                tx.sign(self.user.private_key)
                if tx.isValid():
                    self.tx_pool.add(tx)

                    # REMOVE spent outputs
                    self.user.utxo = self.user.utxo[utxo_i:]
                    self.user.utxo.append([self.user.pem_public_key, sender_change, self.user.username])

                    return
                    self.hf.enterToContinue(f"The transaction has been added to the pool with ID: {tx.id}")


                else:
                    self.hf.enterToContinue(f"ERROR: The transaction could not be added to the transaction pool as it is INVALID")
            else:
                self.hf.enterToContinue("ERROR: User not found")
            # TODO Validate the receiver is not the user
        else:
            self.hf.enterToContinue(f"ERROR: The gas fee must be between 0 and {send_amount}.")

    def checkBalance(self):
        balance = 0
        if self.user.utxo != []:
            print("List of unspend transaction outputs (UTXO):")
            for i, output in enumerate(self.user.utxo):
                balance += output[1]
                print(f"{i+1}. {output[1]}")

        self.hf.enterToContinue(f"Total Balance: {balance}")

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
        #TODO:
        # previous Hash of new block is the unmined hash of the previous block

        # Check if there 5 tx in transaction pool
        if len(self.tx_pool.transactions) < 5:
            self.hf.enterToContinue(f"There are currently {len(self.tx_pool.transactions)} in the transaction pool but at least 5 are required to create block.")
            return

        prev_block = self.blockchain.getPrevBlock()
        new_block =GCBlock(self.tx_pool.getTxData(), prev_block)
        start_time = time.time()
        new_block.mine()
        end_time = time.time() - start_time
        reward_sum = 50 # Base reward
        for tx in new_block.transactions:
            reward_sum += tx.gas_fee
        self.blockchain.add(new_block)
        self.blockchain.save()
        self.tx_pool.removeTx()
        self.tx_pool.save()
        # TODO Add reward transaction / Write function to calculate gas fees.
        tx_reward = GCTx([("REWARD", reward_sum, "Mining Reward")], [(self.user.pem_public_key, reward_sum, self.user.username)])
        self.tx_pool.add(tx_reward)
        self.user.utxo = self.blockchain.calculateUTXO(self.user.pem_public_key)
        #######
        self.hf.enterToContinue(f"{64*'-'}\nMining Succesful with a nonce of: {new_block.nonce}\nHash: {new_block.blockHash}\nTime: {end_time}")

    def viewAccountDetails(self):
        print(f"{64*'='}\nUsername: {self.user.username}\n{64*'-'}\nPublic Key:\n{self.user.pem_public_key.decode('utf-8')}\n{self.user.pem_private_key.decode('utf-8')}\n")
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
