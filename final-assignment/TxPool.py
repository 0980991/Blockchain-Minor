import pickle

class TxPool():
    def __init__(self):
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

    def restorePool(self, data_file="TxPool.dat"):
        fh = open(data_file, 'rb')
        transactions = pickle.load(fh)
        fh.close()
        self.transactions = transactions

    def storePool(self, data_file="TxPool.dat"):
        fh = open(data_file, 'wb')
        pickle.dump(self.transactions, fh)
        fh.close()