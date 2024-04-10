import pickle
from GCBlock import GCBlock
from helper_functions import HelperFunctions
from datetime import datetime as dt
from datetime import timedelta as td


class TxPool():
    def __init__(self):
        self.hf = HelperFunctions()
        self.transactions = []

    def add(self, tx):
        self.transactions.append(tx)
        self.save()

    def clear(self):
        self.transactions = []

    def getUserTransactions(self, username):
        user_transactions = []
        for tx in self.transactions:
            if tx.inputs[0][0] == username:
                user_transactions.append(tx)
        tx_str = ""
        for tx in user_transactions:
            tx_str += 64*"=" + "\n" + str(tx) + "\n"
        return tx_str

    def remove(self, tx_id):
        new_tx_list = [tx for tx in self.transactions if tx.id != tx_id]
        if self.transactions == new_tx_list:
            print("ERROR: Transaction not found. No transaction has been removed")
        self.transactions = new_tx_list

    def load(self, data_file="TxPool.dat"):
        try:
            fh = open(data_file, 'rb')
            transactions = pickle.load(fh)
            fh.close()
            self.transactions = transactions
        except FileNotFoundError:
            print("TxPool.dat not found!")
            # if self.hf.yesNoInput("Error! TxPool.dat could not be located. Make sure it is stored in the same directory as the goodchain.py file\nWould you like to create a new emtpy file?"):
            #     self.save()

    def save(self, data_file="TxPool.dat"):
        fh = open(data_file, 'wb')
        pickle.dump(self.transactions, fh)
        fh.close()

    def sort(self):
        # 0. self.transactions by default is sorted by time since transactions are appended over time.
        # 1. Reward transactions have highest priority
        # 2. Gas fee amount takes second priority*
        # 3. *If a transaction is older than 2 days, it will be prioritized over a high gas fee tx.
        # 4. Multiple transactions older than 2 days will be once again prioritized based on gas fee.
        def sort_key(tx):
            if tx.time_stamp < (dt.now()-td(days=2)):
                return (0, -tx.time_stamp.timestamp())
            else:
                return (1, -tx.gas_fee)

        reward_transactions = []
        regular_transactions = []
        for tx in self.transactions:
            if tx.inputs[0] == "REWARD":
                reward_transactions.append(tx)
            else:
                regular_transactions.append(tx)

        sorted_transactions = sorted(regular_transactions, key=sort_key)
        self.transactions = reward_transactions + sorted_transactions
        return

        for tx in sorted_transactions:
            print(tx.gas_fee)


    def getTxData(self):
        tx_data = self.transactions[:5]
        # REMOVE tx FROM self.transactions.
        return tx_data
    def __str__(self):
        tx_str = ""
        for tx in self.transactions:
            tx_str += 64*"=" + "\n" + str(tx) + "\n"
        return tx_str