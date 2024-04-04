import pickle
from helper_functions import HelperFunctions

class TxPool():
    def __init__(self):
        self.hf = HelperFunctions()
        self.transactions = []

    def add(self, tx):
        self.transactions.append(tx)

    def clear(self):
        self.transactions = []

    def getUserTransactions(self, from_addr):
        user_transactions = []
        for tx in self.transactions:
            if tx.inputs[0][0] == from_addr:
                user_transactions.append(tx)
        return user_transactions

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
            self.hf.yesNoInput("Error! TxPool.dat could not be located. Make sure it is stored in the same directory as the goodchain.py file\nWould you like to create a new emtpy file?")
            self.save()
    def save(self, data_file="TxPool.dat"):
        fh = open(data_file, 'wb')
        pickle.dump(self.transactions, fh)
        fh.close()

    def __str__(self):
        for tx in self.transactions:
            print(tx)