import Signature as sig
from datetime import datetime as dt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

## FOR DEBUG
import time

class GCBlock:
    def __init__(self, data, previousBlock=None):
        self.previousBlock = previousBlock
        self.time_stamp = dt.now()
        self.transactions = data
        self.nonce = 0
        self.leading_zeros = 3
        if previousBlock is None:
            self.id = 0
            self.previousHash = None
        else:
            self.id = previousBlock.id + 1
            self.previousHash = previousBlock.computeHash()
        self.blockHash = self.computeHash()

    def addTx(self, Tx):
        self.transactions.append(Tx)

    def computeHash(self):
        # TODO Add Time stamp and self.id to the hash
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.transactions),'utf8'))
        digest.update(bytes(str(self.previousHash),'utf8'))
        digest.update(bytes(str(self.nonce), 'utf8'))
        h = digest.finalize()
        h = h.hex()
        return h

    def validate(self):
        # 1. Check if tranactions in block are valid
        for tx in self.transactions:
            if not tx.isValid():
                return False
        # 2. Check if previous
        if self.previousBlock == None:
            cur_hash = self.computeHash()
            if self.blockHash == self.computeHash():
                return True
            else:
                return False
        else:
            current_block_validity = self.blockHash == self.computeHash()
            previous_block_validity = self.previousBlock.validate()
            return current_block_validity and previous_block_validity

    def mine(self):
        if self.previousBlock is not None:
            self.previousHash=self.previousBlock.computeHash()
            print()
        zeroes = '0'*self.leading_zeros
        difficulty = 16
        flag = True
        start_time = time.time()
        while flag:
            new_hash = self.computeHash()
            print(new_hash)
            if new_hash.startswith(zeroes):
                if ord(new_hash[self.leading_zeros]) < difficulty: # Multiplies time by 2
                    flag = False
                    break
            self.nonce += 1
            if time.time() - start_time > 10 and self.nonce % 500 == 0 and difficulty < 256:
                print(time.time()-start_time)
                difficulty = difficulty + 10
        self.blockHash = new_hash
        # input(f"{time.time()-start_time}\ndiff: {difficulty}")

    def __str__(self):
        data_str = "\n"
        for tx in self.transactions:
            out_str = ""
            for i, outs in enumerate(tx.outputs):
                if i > 0:
                    out_str += " & "
                out_str += f"{outs[1]} to {outs[2]}"
            data_str += f"  Transaction [{tx.id}]: {tx.inputs[0][1]} from {tx.inputs[0][2]} --> {out_str}\n"
        string =  f"Block [{self.id}]\n{64*'='}\nMined on: {self.time_stamp}"
        string += f"\n{64*'-'}\nData: {data_str}{64*'-'}\n"
        string += f"Nonce: {self.nonce}\n{64*'-'}\nPrevious Block Hash: {self.previousHash}\n{64*'-'}\nCurrent Block Hash: {self.blockHash}\n"
        string += f"{(64*'-')}\n"
        return string