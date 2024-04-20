import random as r
import os
import sys
from GCAccounts import GCAccounts
from GCUser import GCUser
from GCBlock import GCBlock
import HelperFunctions as hf
from DbInterface import DbInterface as dbi
from GCTx import GCTx
from TxPool import TxPool
from BlockChain import BlockChain
import time

## QUESTIONS:
# 1. Does genesis block have to be mined? Does it need a hash of 000

class GoodChainApp():

    def __init__(self, prompt="(guest)> "):
        self.prompt = prompt
        self.accounts = GCAccounts()

        self.tx_pool = TxPool()
        self.tx_pool.load()
        self.tx_pool.sort()

        self.blockchain = BlockChain()
        self.blockchain.load()

        self.logged_in = False
        self.user = None
        self.options = None
        self.setMenuOptions()

    def test(self):
        users = self.accounts.loadUsers()
        user1 = users[0]
        user2 = users[1]
        user3 = users[2]
        tx_1 = GCTx([(user1[0], 50.0, user1[2])],
                         [(user2[0], 40.0, user2[2])],
                         10.0)
        self.tx_pool.add(tx_1)
        # self.tx_pool.sort()
        tx_2 = GCTx([(user2[0], 10.0, user1[2])],
                         [(user2[1], 10.0, user2[2])],
                         0.0)
        self.tx_pool.add(tx_2)
        self.tx_pool.sort()
        tx_3 = GCTx([(user1[0], 10.0, user3[2])],
                         [(user2[1], 1.0, user2[2])],
                         9.0)
        self.tx_pool.add(tx_3)
        # self.tx_pool.sort()
        tx_4 = GCTx([("REWARD", 50.0, "Debug Reward")],
                         [(user3[0], 50.0, user3[2])])
        self.tx_pool.add(tx_4)
        # self.tx_pool.sort()
        tx_5 = GCTx([("REWARD", 50.0, "Debug Reward II ")],
                         [(user1[0], 50.0, user1[2])])
        self.tx_pool.add(tx_5)
        self.tx_pool.sort()

        hf.enterToContinue()
        pass


    def start(self):
        # print*.test()
        while True:
            hf.clear()
            print(self.getBanner())
            choice = hf.optionsMenu("Welcome to the GoodChain application.\nWhat would you like to do?", self.options, prompt=self.prompt)
            self.options[choice][0]()


    def exit(self):
        if self.logged_in:
            if hf.yesNoInput("Are you sure you want Logout and Quit the application?"):
                sys.exit()
            return
        sys.exit()

    def explore(self):
        hf.enterToContinue(str(self.blockchain))

    def login(self):
        user_credentials = hf.readUserInput(["Enter your username:", "Enter your password:"], prompt=self.prompt)
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
                    self.user.utxo = self.blockchain.calculateUTXO(self.user.pem_public_key, self.tx_pool)
                    self.prompt = f"({user.username})> "
                    self.logged_in = True
                    self.setMenuOptions()
                    hf.enterToContinue("\n[+] Login Sucessful!\n")
                    # self.test()
                    return
                else:
                    if hf.yesNoInput("Login Failed! You've entered an incorrect username or password.\nDo you want to try again?"):
                        user_credentials = hf.readUserInput(["Enter your username:", "Enter your password:"], prompt=self.prompt)
                        if user_credentials == []:
                            return
                    else:
                        try_again = False

    def logout(self):
        self.user = None
        self.prompt = "(guest)> "
        self.logged_in = False
        print("\n[+] Logged Out!\n")
        self.setMenuOptions()

    def signUp(self):
        user_credentials = hf.readUserInput(["Enter a username:", "Enter a password:"], prompt=self.prompt)
        if user_credentials == []:
            input("Login canceled!")
            return
        username = user_credentials[0]
        if not self.accounts.userExists(username):
            hashed_pw = self.accounts.hash_string(user_credentials[1])
            new_user = GCUser(username, hashed_pw)
            self.accounts.users.append(new_user)

            dbi.insertUser(new_user)

            tx_reward = GCTx([("REWARD", 50.0, "Signup Reward")], [(new_user.pem_public_key, 50.0, new_user.username)])
            self.tx_pool.add(tx_reward)
            self.tx_pool.sort()

            if hf.yesNoInput("\n[+] Signup Successful!\nDo you want to login now?"):
                self.login()
        else:
            hf.enterToContinue("This username has already been taken!")

    def showUsersDebug(self):
        users_str = ""
        for i, user in enumerate(self.accounts.loadUsers()):
            users_str += f"{i+1}. {user[0]}\n"
        hf.enterToContinue(users_str)

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
                [self.addTransactionsDebug, "Add Tx (DEBUG)"],
                [self.showUsersDebug, "Show all users (DEBUG)"]
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
            tx_reward = GCTx([("REWARD", 50.0, "Debug Reward")], [(self.user.pem_public_key, 50.0, self.user.username)])
            self.tx_pool.add(tx_reward)
            self.tx_pool.sort()
            time.sleep(0.01)
            # while username == self.user.username:
            #     username = r.choice(["joe", "mark", "q", "ari"])
            # send_amount = r.choice([20, 40, 50.0, 1000, 100])
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
                username, amount, gas_fee = hf.readUserInput(["Enter the username of the receiver", "Please enter the amount you would like to transfer", "Please enter the gas fee amount (Gas fee will be subtracted from the transfer amount.)"], prompt=self.prompt)
                valid_input=True
            except ValueError:
                # User canceled and the function returned an empty list.
                return

        send_amount = float(amount)
        gas_fee = float(gas_fee)
        receive_amount = send_amount - gas_fee
        if gas_fee >= 0 and gas_fee < send_amount:
            if self.user.username != username and self.accounts.userExists(username):

                utxo_sum = 0
                utxo_i = 0
                while utxo_sum < send_amount:
                    # TODO utxo_i Currently gives an index error if send amount > current balance
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
                    if hf.yesNoInput(f"==={tx}\nAre you sure you want to create a transaction with the following details?"):
                        self.tx_pool.add(tx)
                        self.tx_pool.sort()

                        # REMOVE spent outputs
                        self.user.utxo = self.user.utxo[utxo_i:]
                        # ADD sender change output to spendable outputs
                        if sender_change != 0:
                            self.user.utxo.append([self.user.pem_public_key, sender_change, self.user.username])

                        hf.enterToContinue(f"The transaction has been added to the pool with ID: {tx.id}")
                        return
                    else:
                        return # User canceled operation


                else:
                    hf.enterToContinue(f"ERROR: The transaction could not be added to the transaction pool as it is INVALID")
            else:
                hf.enterToContinue("ERROR: User not found")
            # TODO Validate the receiver is not the user
        else:
            hf.enterToContinue(f"ERROR: The gas fee must be between 0 and {send_amount}.")

    def checkBalance(self):
        balance = 0
        if self.user.utxo != []:
            print("List of unspend transaction outputs (UTXO):")
            for i, output in enumerate(self.user.utxo):
                balance += output[1]
                print(f"{i+1}. {output[1]}")
        hf.prettyPrint(f"Total Balance: {balance}")
        hf.enterToContinue()

    def viewTransactionPool(self):
        print(self.tx_pool)
        hf.enterToContinue()

    def userTransactions(self):
        usr_tx_str = self.tx_pool.getUserTransactions(self.user.pem_public_key)
        if usr_tx_str == "":
            hf.prettyPrint("You currently have no pending transactions.")
        else:
            print(usr_tx_str)
        tx_id = hf.readUserInput2(f"Enter 'b' to go back\nEnter 'cancel x' (where x is a transaction ID, e.g. 'cancel 20240419113713100785') to cancel a transaction in the transaction pool:", prompt=self.prompt)
        if tx_id == 'b':
            return
        else:
            tx = self.tx_pool.get(tx_id)
            # Check if there is a 'sender change' output in the tx 
            no_sender_change = tx.userInOutputs(self.user.username)
            # Add previously removed output back to the start of the list and REMOVE previously appended output for 'sender change' with pop()
            if self.user.utxo != [] or no_sender_change:
                self.user.utxo.pop()
            old_utxo = [tx.inputs[0]]
            self.user.utxo = old_utxo + self.user.utxo
            self.tx_pool.remove(tx_id)
            self.tx_pool.save()
            hf.enterToContinue(hf.prettyString(f"Transaction [{tx_id}]: Canceled Sucesfully!"))
            return

    def mineBlock(self):
        #TODO:
        # previous Hash of new block is the unmined hash of the previous block

        # Check if there 5 tx in transaction pool
        if len(self.tx_pool.transactions) < 5:
            hf.enterToContinue(f"There are currently {len(self.tx_pool.transactions)} in the transaction pool but at least 5 are required to create block.")
            return

        prev_block = self.blockchain.latest_block
        verbose = hf.yesNoInput("\nShow hash output when mining?")
        print("\n<...Mining in progress...>\n")
        new_block  = GCBlock(self.tx_pool.getTxData(), prev_block)
        start_time = time.time()
        new_block.mine(verbose)
        end_time = time.time() - start_time
        # hf.logEvent(f"{64*"-"}\nNew Block Mined:\n{new_block.id} with hah: {new_block.blockHash}")
        reward_sum = 50.0 # Base reward
        for tx in new_block.transactions:
            reward_sum += tx.gas_fee
        self.blockchain.add(new_block)
        self.blockchain.save()
        self.tx_pool.removeTx()
        self.tx_pool.save()
        tx_reward = GCTx([("REWARD", reward_sum, "Mining Reward")], [(self.user.pem_public_key, reward_sum, self.user.username)])
        self.tx_pool.add(tx_reward)
        self.tx_pool.sort()

        self.user.utxo = self.blockchain.calculateUTXO(self.user.pem_public_key, self.tx_pool)
        #######
        hf.enterToContinue(f"{64*'-'}\nMining Succesful with a nonce of: {new_block.nonce}\nHash: {new_block.blockHash}\nTime: {end_time}\nYour Mining Reward: {reward_sum}")

    def viewAccountDetails(self):
        print(f"{64*'='}\nUsername: {self.user.username}\n{64*'-'}\nPublic Key:\n{self.user.pem_public_key.decode('utf-8')}\n{self.user.pem_private_key.decode('utf-8')}\n")
        hf.enterToContinue()


    def getBanner(self):
        banners = []
        with open(".\\banners.txt", 'r', encoding='utf-16le') as file:
            banners_text = file.read()
            banners = banners_text.split('\n,\n')
        return r.choice(banners)

if __name__ == "__main__":
    app = GoodChainApp()
    app.start()
