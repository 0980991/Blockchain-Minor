import Signature as sig
from datetime import datetime as dt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

class GCBlock:
    def __init__(self, data, previousBlock=None):
        self.time_stamp = dt.now()
        self.data = data
        self.nonce = 0
        self.previousBlock = previousBlock
        self.leading_zeros = 2
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
        h = digest.finalize()
        return h.hex

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
        flag = True
        # new_hash = ''
        while flag:
            new_hash = self.computeHash()
            if new_hash.startswith(zeroes):
                flag = False
            else:
                self.nonce += 1
        self.blockHash = new_hash
            
        # digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        # digest.update(bytes(str(self.data), "utf8"))
        # digest.update(bytes(str(self.previousHash), "utf8"))
        # flag = False
        # nonce = 0
        # while not flag:
        #     digest_temp = digest.copy()
        #     digest_temp.update(bytes(str(nonce), 'utf8'))
        #     block_hash = digest_temp.finalize()
        #     block_hash1 = base64.b64encode(block_hash)
        #     block_hash1 = block_hash1.decode('utf-8')
        #     print(block_hash)
        #     if block_hash[:self.leading_zeros] == bytes('0' * self.leading_zeros, 'utf8'):
        #         if int(block_hash[self.leading_zeros]) < 128: # Multiplies time by 2
        #             flag=True
        #             self.nonce = nonce
        #     nonce  += 1
        #     del digest_temp


        # self.blockHash = self.computeHash()
        # return