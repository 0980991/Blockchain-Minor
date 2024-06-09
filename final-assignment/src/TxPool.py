import pickle
from pickle import UnpicklingError
from GCBlock import GCBlock
import HelperFunctions as hf
from datetime import datetime as dt, timedelta
import sys
import os


class TxPool():
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.normpath(os.path.join(self.base_dir, '..', 'data', 'TxPool.dat'))
        self.transactions = []
        self.load()
        self.sort()

    def add(self, tx):
        self.transactions.append(tx)
        self.save()

    def clear(self):
        self.transactions = []

    def getUserTransactions(self, pem_public_key):
        user_transactions = []
        for tx in self.transactions:
            if tx.inputs[0][0] == pem_public_key:
                user_transactions.append(tx)
        return user_transactions

    def purgeInvalidUserTx(self, pem_public_key):
        user_return_sum = 0
        tx_ids_to_remove = []
        for tx in self.transactions:
            if tx.inputs[0][0]==pem_public_key and not tx.isValid():
                user_return_sum += tx.inputs[0][1] - tx.outputs[-1][1]
                tx_ids_to_remove.append(tx.id)



        for tx_id in tx_ids_to_remove:
            self.remove(tx_id)

        return (tx_ids_to_remove, user_return_sum)

    def remove(self, tx_id):
        new_tx_list = [tx for tx in self.transactions if tx.id != tx_id]
        if self.transactions == new_tx_list:
            print("ERROR [!]: Transaction not found. No transaction has been removed")
        self.transactions = new_tx_list

    def load(self):
        try:
            fh = open(self.data_path, 'rb')
            transactions = pickle.load(fh)
            fh.close()
            self.transactions = transactions
        except FileNotFoundError:
            # TODO: Add to notification section

            hf.enterToContinue("TxPool.dat not found!\nIf the system is launched for the first time the file will be created automatically.\nIf the TxPool.dat file already exists in the 'data' folder, make sure the 'goodchain.py' is launched from the root directory!")
            # if hf.yesNoInput("Error! TxPool.dat could not be located. Make sure it is stored in the same directory as the goodchain.py file\nWould you like to create a new emtpy file?"):
            #     self.save()
        except UnpicklingError:
            hf.enterToContinue("ERROR [!]: TxPool.dat has been corrupted and cannot be opened.\n Please delete the file and restart the program.")
            sys.exit()

    def save(self):
        fh = open(self.data_path, 'wb')
        pickle.dump(self.transactions, fh)
        fh.close()

    def sort(self):
        # 0. self.transactions by default is sorted by time since transactions are appended over time.
        # 1. Once sorted, reward transactions have highest priority
        # 2. Gas fee amount takes second priority*
        # 3. *If a transaction is older than 2 days, it will be prioritized over a high gas fee tx.
        # 4. Multiple transactions older than 2 days will be once again prioritized based on gas fee.
        def sort_key(tx):
            if tx.time_stamp < (dt.now()-timedelta(days=2)):
                return (0, -tx.time_stamp.timestamp())
            else:
                return (1, -tx.gas_fee)

        reward_transactions = []
        regular_transactions = []
        for tx in self.transactions:
            if tx.inputs[0][0] == "REWARD":
                reward_transactions.append(tx)
            else:
                regular_transactions.append(tx)
        regular_transactions.reverse()
        sorted_transactions = sorted(regular_transactions, key=sort_key)

        self.transactions = reward_transactions + sorted_transactions
        return

    def removeTx(self):
        self.transactions = self.transactions[10:]

    def get(self, tx_id):
        for tx in self.transactions:
            if tx.id == tx_id:
                return tx
        return None

    def getTxData(self):
        tx_data = self.transactions[:10]
        return tx_data

    def __str__(self):
        tx_str = ""
        if self.transactions == []:
            return hf.prettyString("The transaction pool is currently empty.")

        for i, tx in enumerate(self.transactions):
            tx_str += f"\n\n[{i+1}] " + str(tx) + "\n"
        return tx_str