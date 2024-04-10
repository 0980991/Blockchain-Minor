import Signature as sig
from datetime import datetime as dt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

## FOR DEBUG
import time

class GCBlock:
    def __init__(self, data, previousBlock=None):
        self.time_stamp = dt.now()
        self.data = data
        self.nonce = 0
        self.previousBlock = previousBlock
        self.leading_zeros = 3
        if previousBlock is None:
            self.previousHash = None
        else:
            self.previousHash = previousBlock.computeHash()
        self.blockHash = self.computeHash()

    def addTx(self, Tx):
        self.data.append(Tx)

    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previousHash),'utf8'))
        digest.update(bytes(str(self.nonce), 'utf8'))
        h = digest.finalize()
        h = h.hex()
        return h

    def validate(self):
        # 1. Check if tranactions in block are valid
        for tx in self.data:
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
        # for _ in range(500000):                    # CAN BE any range         # This lenght can differ and should not affect the time it takes to find it.
            # self.nonce = ''.join([chr(random.randint(48, 123)) for _ in range(10*leading_zeros)])
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