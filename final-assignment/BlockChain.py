from datetime import datetime as dt
from GCBlock import GCBlock
import pickle
class BlockChain:

    def __init__(self):
        self.chain = None
        self.latest_block = None

    def add(self, block):
        self.latest_block = block

    def add2(self, block):
        self.chain.append(block)

    def calculateUTXO(self, pem_public_key, tx_pool):
        utxo = []
        utxo_in = []
        utxo_out = []

        # Start from the latest block (most recent) and iterate backward
        block = self.latest_block
        while block is not None:
            for tx in block.transactions:
                for output in tx.outputs:
                    if output[0] == pem_public_key and output[1] > 0:
                        utxo.append(output)
                        utxo_out.append(output[1])

                for inp in tx.inputs:
                    if inp[0] == pem_public_key:
                        utxo_in.append(inp[1])

            # Move to the previous block
            block = block.previousBlock

        for tx in tx_pool.transactions:
            for output in tx.outputs:
                if output[0] == pem_public_key:
                    utxo.append(output)
                    utxo_out.append(output[1])

                for inp in tx.inputs:
                    if inp[0] == pem_public_key:
                        utxo_in.append(inp[1])
        out_sum = 0
        i = 0
        while out_sum < sum(utxo_in):
            out_sum += utxo_out[i]
            i += 1
        utxo = utxo[i:]
        return utxo

    def load(self, data_file="BlockChain.dat"):
        try:
            fh = open(data_file, 'rb')
            latest_block = pickle.load(fh)
            fh.close()
            self.latest_block = latest_block
        except FileNotFoundError:
            print("Block chain data file not located! A new blockchain will be created.")
            self.latest_block = GCBlock([], None)
        # self.latest_block = self.chain[-1]
        
    def save(self, data_file="BlockChain.dat"):
        fh = open(data_file, 'wb')
        pickle.dump(self.latest_block, fh)
        fh.close()


    def __str__(self):
        block_str = []

        block = self.latest_block
        while block is not None:
            block_str.append(str(block))
            block = block.previousBlock
        block_str.reverse()
        return "\n\n".join(block_str)