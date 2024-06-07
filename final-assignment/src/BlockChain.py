from datetime import datetime as dt, timedelta
from GCBlock import GCBlock
import pickle
from pickle import UnpicklingError
import HelperFunctions as hf
import sys

class BlockChain:

    def __init__(self):
        self.latest_block = None

    def add(self, block):
        self.latest_block = block
        
    def check_duplicate_and_add(self, block):
        # Traverse the chain to find a block with the same ID
        current_block = self.latest_block
        while current_block is not None:
            if current_block.id == block.id:
                if current_block.time_stamp > block.time_stamp:
                    # Replace the current block with the new block
                    self.replace_block(current_block, block)
                    print("duplicate block detected and replaced!!")
                return
            current_block = current_block.previous_block
        
        # If no block with the same ID is found, add the new block
        block.previous_block = self.latest_block
        self.add(block)

    def replace_block(self, old_block, new_block):
        if old_block.previous_block is not None:
            new_block.previous_block = old_block.previous_block
        else:
            new_block.previous_block = None
        if self.latest_block == old_block:
            self.latest_block = new_block


    def calculateBalance(self, username, tx_pool):
        block = self.latest_block
        total_balance = 0
        while block is not None:
            # Only count transaction outputs of validated blocks

            if block.getValidationBools().count(True) > 2:
                for tx in block.transactions:
                    for output in tx.outputs:
                        if output[2] == username:
                            if tx.inputs[0][2] == username:
                                total_balance += tx.inputs[0][1]
                                # return # First block found where the entire user wallet was sent as change
                            else:
                                total_balance += output[1] # Add ouputs from other users
            else:
                # Count spent amount
                for tx in tx_pool.transactions:
                    if tx.inputs[0][2] == username:
                        total_balance -= tx.inputs[0][1] - tx.outputs[-1][1]
            block = block.previous_block
        # Subtract the inputs in currently in tx pool
        for tx in tx_pool.transactions:
            if tx.inputs[0][2] == username and tx.isValid(self.latest_block.previous_block):
                total_balance -= tx.inputs[0][1] - tx.outputs[-1][1]
        return total_balance

    def getTxAmount(self):
        tx_counter = 0
        block = self.latest_block
        while block.previous_block is not None:
            tx_counter += len(block.transactions)
            block = block.previous_block
        return tx_counter

    def getUserTransactions(self, pem_public_key):
        block = self.latest_block
        user_transactions = []
        while block.previous_block is not None:
            for tx in block.transactions:
                if tx.inputs[0][0] == pem_public_key:
                    user_transactions.append(tx)
            block = block.previous_block

        return user_transactions

    def load(self, data_file="data/BlockChain.dat"):
        try:
            fh = open(data_file, 'rb')
            latest_block = pickle.load(fh)
            fh.close()
            self.latest_block = latest_block
        except FileNotFoundError:
            print("Block chain data file not located! A new blockchain will be created.")
            hf.enterToContinue("BlockChain.dat not found!\nIf the system is launched for the first time the file will be created automatically.\nIf the BlockChain.dat file already exists in the 'data' folder, make sure the 'goodchain.py' is launched from the root directory!")

            self.latest_block = GCBlock([], None)
        except UnpicklingError:
            hf.enterToContinue("BlockChain.dat has been corrupted and can no longer be read.\nDelete the file and restart the program!")
            sys.exit()

    def save(self, data_file="data/BlockChain.dat"):
        fh = open(data_file, 'wb')
        pickle.dump(self.latest_block, fh)
        fh.close()

    def miningAllowed(self, tx_pool, print_output=True):
        output_flags = []
        # Check if there 5 tx in transaction pool
        if len(tx_pool.transactions) >= 5:
            output_flags.append((True, ""))
        else:
            output_flags.append((False, f"ERROR [!]: There are currently {len(tx_pool.transactions)} transactions in the transaction pool but at least 5 are required to create block"))
        # Check if previous block has all valid flags
        if self.latest_block.getValidationBools().count(True) > 2:
            output_flags.append((True, ""))
        else:
            output_flags.append((False, f"ERROR [!]: Previous Block has not yet been fully verified!\nMake sure the previous block has been validated by 3 users.\nCurrently {self.latest_block.getValidationBools().count(True)}/3 have validated the block."))

        # Check if previous block has been mined longer than 3 minutes ago
        time_since_last_block = dt.now() - self.latest_block.time_stamp
        if time_since_last_block > timedelta(minutes=3):
            output_flags.append((True, ""))
        else:
            output_flags.append((False, f"ERROR [!]: It has only been {time_since_last_block} since the previous block was mined! Please wait 3 minutes before mining the next block. "))

        bool_flags = []
        for flag in output_flags:
            bool_flags.append(flag[0])
            if print_output:
                print(flag[1])
        return all(bool_flags)

    def validate(self):
        return self.latest_block.validate()

    def __str__(self):
        block_str = []

        block = self.latest_block
        while block is not None:
            block_str.append(str(block))
            block = block.previous_block
        block_str.reverse()
        return "\n\n".join(block_str)