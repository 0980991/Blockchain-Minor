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
import server
import client
import threading
import datetime
import asyncio

## FOR DEBUG
import inspect

class GoodChainApp():

    def __init__(self, prompt="(guest)> "):
        self.prompt = prompt
        self.accounts = GCAccounts()

        self.tx_pool = TxPool()
        # self.tx_pool.load()
        # self.tx_pool.sort()


        self.blockchain = BlockChain()
        self.blockchain.load()
        
        # server_thread = threading.Thread(target=server.start_server, daemon=True)
        # server_thread.start()

        self.logged_in = False
        self.user = None
        self.options = None
        self.notifications = []
        self.setMenuOptions()

        # server_thread = threading.Thread(target=server.start_server, daemon=True, args=(self,))
        # server_thread.start()


    def start(self):
        while True:
            print(self.getBanner())
            if self.logged_in:
                    self.defaultNodeActions()
            if self.blockchain.latest_block.getValidationBools().count(True) < 3:
                self.notifications.append(f"The most recently mined block {self.blockchain.latest_block.id} is still pending for verification. Flags: {self.blockchain.latest_block.getValidationBools().count(True)}/3")
            else:
                if self.blockchain.miningAllowed(self.tx_pool, False):
                    self.notifications.append("[!] A new block can be mined")
            self.notifications.append(f"Number of blocks in chain: {self.blockchain.latest_block.id}")
            self.notifications.append(f"Number of transactions in chain: {self.blockchain.getTxAmount()}")
            n_str = "NOTIFICATIONS:\n"
            for i, notification in enumerate(self.notifications):
                n_str += f"--> {i+1}. {notification}\n"

            self.notifications = []
            # If block unmined
            choice = hf.optionsMenu(f"\n{n_str}\n\nWhat would you like to do?\n(Select an option by typing 1-{len(self.options)} and pressing 'Enter'.)", self.options, prompt=self.prompt)
            self.options[choice][0]()

    def defaultNodeActions(self):
        # 1. Validate latest mined block
        # 2. Delete block if marked invalid
        # 3. Purge invalid tx in pool (validates chain)
        
        # Perform default node actions:
        # 1. Validate newly mined block if necessary and if not mined by user and user hasnt already validated the block
        if not self.blockchain.latest_block.getValidationBools().count(True) > 2 and self.blockchain.latest_block.mined_by != self.user.username and not self.blockchain.latest_block.userHasAlreadyValidated(self.user.username):
            for i, flag in enumerate(self.blockchain.latest_block.validation_flags):
                if flag[0] is None:
                    if self.blockchain.validate(): # This checks whether the latest block is valid
                        self.blockchain.latest_block.validation_flags[i] = [True, self.user.username]
                        self.blockchain.save()
                        notification_msg = f"You have validated flag {i+1}/3 of the latest block in the chain: Block [{self.blockchain.latest_block.id}]"
                        self.notifications.append(notification_msg)
                        # self.options[0]
                        # Create MINING REWARD transaction if the last flag has been validated and the previous block is not the genesis block.
                        if i == 2 and self.blockchain.latest_block.previous_block is not None:
                            receiver_username = self.blockchain.latest_block.mined_by
                            receiver_pem_public_key = self.accounts.publicKeyFromUsername(receiver_username)
                            reward_sum = self.blockchain.latest_block.getRewardSum()
                            tx_reward = GCTx([("REWARD", reward_sum, "Mining Reward")], [(receiver_pem_public_key, reward_sum, receiver_username)])
                            # Verify tx before adding to pool.
                            if tx_reward.isValid(self.blockchain.latest_block):
                                self.tx_pool.add(tx_reward)
                                self.tx_pool.sort()
                                self.tx_pool.save()

                                # Update the current user balance in case to reflect the transactions in the newly accepted block
                                self.user.balance = self.blockchain.calculateBalance(self.user.username, self.tx_pool)

                                notification_msg = f"You have created a reward transaction for {self.blockchain.latest_block.mined_by} for mining Block [{self.blockchain.latest_block.id}]"
                                self.notifications.append(notification_msg)
                    else:
                        self.blockchain.latest_block.validation_flags[i] = [False, self.user.username]
                        notification_msg = f"You have invalidated flag {i+1}/3 of the latest block in the chain: Block [{self.blockchain.latest_block.id}]"
                        self.notifications.append(notification_msg)
                        # 2. Check if block is fully invalidated and delete it if it is.
                        if i == 2 and self.latest_block.previous_block is not None:
                            for tx in self.blockchain.latest_block.transactions:
                                # Add all valid transactions from the deleted block back to the TX pool if they are valid.
                                if tx.isValid(self.blockchain.latest_block):
                                    self.tx_pool.append(tx)
                                else:
                                    #Return funds (Refunds for other users are calculate when they login)
                                    if tx.inputs[0][0] == self.user.pem_public_key:
                                        self.user.balance += tx.inputs[0][1] - tx.outputs[-1][1]
                            self.tx_pool.sort()
                            self.tx_pool.save()
                            self.blockchain.latest_block = self.blockchain.latest_block.previous_block
                    break
                print()
        # elif self.blockchain.latest_block.validation_flags.count(False) > 2:
        #     # TODO: Remove Block and return transactions



        # 3. Remove any INVALiD transactions in pool (Detects tampering since a tx can only be added to the pool if it is valid)
        removed_tx_ids, user_return_sum = self.tx_pool.purgeInvalidUserTx(self.user.pem_public_key, self.blockchain.latest_block)

        if removed_tx_ids != []:
            notification_msg = f"Your transactions: {''.join([tx_id + ', ' if index < len(removed_tx_ids) - 1 else tx_id for index, tx_id in enumerate(removed_tx_ids)])} are invalid and have been deleted from the transaction pool."
            self.notifications.append(notification_msg)
        self.user.balance += user_return_sum


    def exit(self):
        if self.logged_in:
            if hf.yesNoInput("Are you sure you want Logout and Quit the application?"):
                sys.exit()
            return
        sys.exit()


    def explore(self):
        self.blockchain.load()
        hf.enterToContinue(str(self.blockchain))

    async def check_nodes(self, user):
        return await (client.send_data("logged_in", user))

    def login(self):
        self.accounts.loadUsers()
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
                    if asyncio.run(self.check_nodes(user.username)):
                        hf.enterToContinue("\n[+] your are already logged in on another node!\n")
                        return
                if user is not None:
                    self.user = user
                    self.user.balance = self.blockchain.calculateBalance(self.user.username, self.tx_pool)
                    self.prompt = f"({user.username})> "
                    self.logged_in = True
                    self.setMenuOptions()
                    hf.enterToContinue("\n[+] Login Sucessful!\n")
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
            sendable_user = new_user
            sendable_user.private_key = None
            sendable_user.public_key = None
            # client.send_data("user_add", sendable_user)

            tx_reward = GCTx([("REWARD", 50.0, "Signup Reward")], [(new_user.pem_public_key, 50.0, new_user.username)])
            if tx_reward.isValid():
                self.tx_pool.add(tx_reward)
                self.tx_pool.sort()
                # client.send_data("transaction_add", tx_reward)

                if hf.yesNoInput("\n[+] Signup Successful!\nDo you want to login now?"):
                    self.login()
            else:
                hf.enterToContinue(f"ERROR: The reward transaction for new user '{new_user.username}' has been invalidated. Possibly due to tampering.")
        else:
            hf.enterToContinue("ERROR: This username has already been taken!")

    # def showUsersDebug(self):
    #     users_str = ""
    #     for i, user in enumerate(self.accounts.loadUsers()):
    #         users_str += f"{i+1}. {user[0]}\n"
    #     hf.enterToContinue(users_str)

    def setMenuOptions(self):
        if self.logged_in:
            self.options = [
                [self.explore, "Explore the Blockchain"],
                [self.transfer, "Create a Transaction"],
                [self.viewTransactionPool, "View Transaction Pool"],
                [self.userTransactions, "Your Pending Transactions"],
                [self.userTransactionHistory, "Your Transaction History"],
                [self.mineBlock, "Mine a Block"],
                [self.viewAccountDetails, "View your Account Details (Balance, Private/Public key)"],
                [self.logout, "Logout"],
                [self.exit, "Exit"]
                # [self.runSimDebug, "Run Mining Simulation (DEBUG)"],
                # [self.showUsersDebug, "Show all users (DEBUG)"]
            ]
        else:
            self.options = [
                [self.login, "Login"],
                [self.explore, "Explore the Blockchain"],
                [self.viewTransactionPool, "View Transaction Pool"],
                [self.signUp, "Sign Up"],
                [self.exit,"Exit"]
            ]

    # def runSimDebug(self):
    #     times = []
    #     nr_blocks = int(input("enter nr of blocks" + "\n" + self.prompt))
    #     for j in range(nr_blocks):
    #         for i in range(5):
    #             user = self.accounts.users[i]
    #             if i==0:
    #                 user.balance = 500
    #             if i != 0:
    #                 user2 = self.accounts.users[0]
    #             else:
    #                 user2 = self.accounts.users[2]
    #             # tx_reward = GCTx([("REWARD", 50.0, "Debug Reward")], [(self.user.pem_public_key, 50.0, self.user.username)])
    #             amount =  r.uniform(10.0, 100.0)
    #             gas_fee = amount/10
    #             tx_reward = GCTx([(user.pem_public_key, amount, user.username)], [(user2.pem_public_key, amount, user2.username)], gas_fee)
    #             tx_reward.sign(user.private_key)
    #             self.tx_pool.add(tx_reward)
    #             self.tx_pool.sort()
    #             time.sleep(0.01)
    #         times.append(self.mineBlock())
    #     times.sort()
    #     times.reverse()
    #     for t in times:
    #         print(t)
    #     hf.enterToContinue()


    def transfer(self):
        valid_input = False
        back_flag = True
        while not valid_input:
            try:
                username, amount, gas_fee = hf.readUserInputTransaction(prompt=self.prompt, initial_balance=self.user.balance)
                back_flag = False
                send_amount = float(amount)
                gas_fee = float(gas_fee)
                valid_input=True
            except ValueError:
                # User canceled and the function returned an empty list.
                if back_flag:
                    return
                hf.enterToContinue("ERROR [!]: The amount and gas fee must be a numerical value.")


        check_send_amount = send_amount > 0
        check_gas_fee = gas_fee >= 0
        check_usr_balance = self.user.balance >= send_amount + gas_fee
        if check_send_amount and check_gas_fee and check_usr_balance:
            if self.user.username != username and self.accounts.userExists(username):

                sender_change = self.user.balance - send_amount - gas_fee
                tx = GCTx([(self.user.pem_public_key, self.user.balance, self.user.username)],
                        [(self.accounts.publicKeyFromUsername(username), send_amount, username), (self.user.pem_public_key,sender_change, self.user.username)],
                        gas_fee)

                tx.sign(self.user.private_key)

                if tx.isValid():
                    if hf.yesNoInput(f"==={tx}\nAre you sure you want to create a transaction with the following details?"):
                        self.tx_pool.add(tx)
                        self.tx_pool.sort()

                        # REMOVE spent outputs
                        self.user.balance -= send_amount + gas_fee
                        hf.enterToContinue(f"The transaction has been added to the pool with ID: {tx.id}")
                        # client.send_data("transaction_add", tx)
                        return
                    else:
                        return # User canceled operation


                else:
                    hf.enterToContinue(f"ERROR [!]: The transaction could not be added to the transaction pool as it is INVALID")
            else:
                hf.enterToContinue("ERROR [!]: User not found OR You've entered your own username")
        else:
            msg = ""
            if not check_send_amount:
                msg += "\tThe send amount is greater than 0.0\n"
            if not check_gas_fee:
                msg += "\tThe gas fee amount is greater than or equal to than 0 and less than the amount you want to send.\n"
            if not check_usr_balance:
                msg += f"\tThe send amount is smaller than your balance. You can only spend up to {self.user.balance}"
            hf.enterToContinue(f"ERROR [!]: Make sure that:\n{msg}.")

    def viewTransactionPool(self):
        self.tx_pool.load()
        print(self.tx_pool)
        hf.enterToContinue()

    def userTransactionHistory(self):
        user_tx_pool = self.tx_pool.getUserTransactions(self.user.pem_public_key)
        user_tx_blockchain = self.blockchain.getUserTransactions(self.user.pem_public_key)

        tx_str = "Transactions currently in the Transaction Pool:\n"
        for i, tx in enumerate(user_tx_pool):
            tx_str += f"[{i+1}] {str(tx)}\n"
        if user_tx_pool != []:
            print(tx_str)
        else:
            print("<Currently no transactions in the transaction pool>")

        tx_str = "Transactions in the blockchain:\n"
        for i, tx in enumerate(user_tx_blockchain):
            tx_str += f"[{i+1}] {str(tx)}\n"
        if user_tx_blockchain != []:
            print(tx_str)
        else:
            print("<Currently no transactions in the blockchain!")
        hf.enterToContinue()

    def userTransactions(self):
        usr_tx = self.tx_pool.getUserTransactions(self.user.pem_public_key)
        if usr_tx == []:
            hf.prettyPrint("You currently have no pending transactions.")
        else:
            tx_str = ""
            for i, tx in enumerate(usr_tx):
                tx_str += f"[{i+1}] " + 60*"=" + "\n" + str(tx) + "\n"
            print(tx_str)
        print("\nTo cancel a transaction, copy the transaction ID and use the 'cancel' command to cancel it")
        tx_id = hf.readUserInput2(f"Enter 'b' to go back\nEnter 'cancel x' (where x is a transaction ID, e.g. 'cancel 20240419113713100785') to cancel a transaction in the transaction pool:", prompt=self.prompt)
        if tx_id == 'b':
            return
        else:
            tx = self.tx_pool.get(tx_id)
            if tx.inputs[0][0] == self.user.pem_public_key:
                self.user.balance += tx.inputs[0][1] - tx.outputs[-1][1]
            else:
                hf.enterToContinue("ERROR [!]: You can only delete your own transactions from the pool!")
                return
            self.tx_pool.remove(tx_id)
            self.tx_pool.save()
            hf.enterToContinue(hf.prettyString(f"Transaction [{tx_id}]: Canceled Sucesfully!"))
            return

    def mineBlock(self):
        mining_allowed = self.blockchain.miningAllowed(self.tx_pool)
        if mining_allowed:
            prev_block = self.blockchain.latest_block
            verbose = hf.yesNoInput("Show hash output when mining?")
            print("\n<...Mining in progress...>\n")
            new_block  = GCBlock(self.tx_pool.getTxData(), prev_block)
            new_block.mined_by = self.user.username
            start_time = time.time()
            new_block.mine(verbose)
            end_time = time.time() - start_time

            self.blockchain.check_duplicate_and_add(new_block)
            self.blockchain.save()
            self.tx_pool.removeTx()
            self.tx_pool.save()
            client.send_data("block_add", new_block)

            self.notifications.append(f"You have mined the latest block [BLOCK {new_block.id}]\nA transaction for your mining reward of {new_block.getRewardSum()} will be added to the transaction pool when all flags have been validated.")
            self.setMenuOptions()
            hf.enterToContinue(f"{64*'-'}\nMining Succesful with a nonce of: {new_block.nonce}\nHash: {new_block.blockHash}\nTime: {end_time}\nYour Mining Reward: {new_block.getRewardSum()}")
            return end_time
        else:
            hf.enterToContinue()

    def viewAccountDetails(self):
        while True:
            print(f"{64*'='}\n{64*'-'}\nPublic Key:\n{self.user.pem_public_key.decode('utf-8')}\n{self.user.pem_private_key.decode('utf-8')}\nUsername: {self.user.username}\n{hf.prettyString(f'Balance: {self.user.balance}')}\n")
            new_pw = hf.readUserInput3(f"To Change your password type 'changepw' and hit enter.\nEnter 'b' to go back\n", prompt=self.prompt)
            if new_pw == 'b':
                return
            else:
                if not new_pw == "":
                    hashed_pw = self.accounts.hash_string(new_pw)
                    self.user.pw_hash = hashed_pw
                    dbi.updatePwHash(self.user.username, hashed_pw)
                    client.send_data("user_changepw",
                    {
                    "username": self.user.username,
                    "password": hashed_pw
                    })

                    hf.enterToContinue(hf.prettyString("Password sucesfully updated!"))

    def getBanner(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        banners_file_path = os.path.normpath(os.path.join(script_dir, '..', 'banners.txt'))

        banners = []
        with open(banners_file_path, 'r', encoding='utf-16le') as file:
            banners_text = file.read()
            banners = banners_text.split('\n,\n')
        return r.choice(banners)

    def validateChain(self):
        if self.blockchain.validate(): # TODO this might not check the whole chain
            message = "Your version of the GoodChain is VALID!"
        else:
            message = "Your version of the GoodChain is INVALID!"
        hf.enterToContinue(hf.prettyString(message))

    def viewNotifications(self):
        output_str = ""
        for i, n in enumerate(self.user.notifications):
            output_str += f"{i+1}. {n}\n"

        hf.enterToContinue(output_str)

if __name__ == "__main__":
    app = GoodChainApp()
    app.start()
