from datetime import datetime as dt
from GCBlock import GCBlock
import pickle
class BlockChain:

    def __init__(self, chain_data_file="BlockChain.dat"):
        self.chain_data_file = chain_data_file
        try:
            fh = open(chain_data_file, 'rb')
            blockchain = pickle.load(fh)
            fh.close()
            self.chain = blockchain
        except FileNotFoundError:
            print("Block chain data file not located! A new blockchain will be created.")
            self.chain = [GCBlock([], None)]
            # if self.hf.yesNoInput("Error! TxPool.dat could not be located. Make sure it is stored in the same directory as the goodchain.py file\nWould you like to create a new emtpy file?"):
            #     self.save()

    def add(self, block):
        self.chain.append(block)

    def calculateUTXO(self, pem_public_key):
        utxo = []
        for block in self.chain:
            for tx in block.transactions:
                for output in tx.outputs:
                    if output[0] == pem_public_key and output[1] > 0:
                        utxo.append(output)
                        
        return utxo

    def getUserBalance(self, user):
        balance = 0
        # Iterate through the chain in reverse
        for i in range(len(self.chain) - 1, -1, -1):
            print(my_list[i])
        # for block in self.chain:
        #     for transaction in block.transactions:
        #         if transaction['from'] == address:
        #             balance -= transaction['amount']
        #             balance -= transaction['gas']
        #         if transaction['to'] == address:
        #             balance += transaction['amount']

        return balance

    def load(self, data_file="BlockChain.dat"):
        try:
            fh = open(data_file, 'rb')
            transactions = pickle.load(fh)
            fh.close()
            self.transactions = transactions
        except FileNotFoundError:
            print(f"{data_file} not found!")

    def save(self, data_file="BlockChain.dat"):
        fh = open(data_file, 'wb')
        pickle.dump(self.chain, fh)
        fh.close()

    def getPrevBlock(self):
        return self.chain[-1]

    def __str__(self):
        string = ""
        for block in self.chain:
            string += str(block) + "\n\n"
        string = string[2:]
        return string