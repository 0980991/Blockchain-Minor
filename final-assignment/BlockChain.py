from datetime import datetime as dt
from GCBlock import GCBlock
class BlockChain:

    def __init__(self, chain_data_file="GoodChain.dat"):
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

    def load(self, data_file):
        pass

    def save(self, data_file="BlockChain.dat"):
        pass

    def getPrevBlock(self):
        return self.chain[-1]
