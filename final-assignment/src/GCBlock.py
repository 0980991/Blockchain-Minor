import Signature as sig
from datetime import datetime as dt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64


## FOR DEBUG
import inspect
import os
import time
import HelperFunctions as hf


class GCBlock:
    def __init__(self, data, previous_block=None):
        self.previous_block = previous_block
        self.time_stamp = dt.now()
        self.transactions = data
        self.nonce = 0
        self.leading_zeros = 3
        self.validation_flags = [[None, ""], [None, ""], [None, ""]]
        self.mined_by = ""
        if previous_block is None:
            self.id = 0
            self.previous_hash = None
            self.mined_by = "SYSTEM"
        else:
            self.id = previous_block.id + 1
            self.previous_hash = previous_block.blockHash
        new_block_hash = self.computeHash(True)
        self.blockHash = new_block_hash

    def addTx(self, Tx):
        self.transactions.append(Tx)

    def computeHash(self, log=False):
        tx_str = ""
        for tx in self.transactions:
            tx_str+=str(tx.collectTxData())
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.id), 'utf8'))
        digest.update(bytes(str(self.time_stamp), 'utf8'))
        digest.update(bytes(tx_str,'utf8'))
        digest.update(bytes(str(self.previous_hash),'utf8'))
        digest.update(bytes(str(self.nonce), 'utf8'))
        h = digest.finalize()
        h = h.hex()
        if log:
            log_str = 64*"-" + "\n"
            log_str += f"{str(self.id)}\n{str(tx_str)}\n{str(self.previous_hash)}\n{str(self.nonce)}"
        return h

    def userHasAlreadyValidated(self, username):
        for flag in self.validation_flags:
            if flag[1] == username:
                return True

    def getRewardSum(self):
        reward_sum = 50.0
        for tx in self.transactions:
            reward_sum += tx.gas_fee
        return reward_sum

    def getValidationBools(self):
        bools = []
        for flag in self.validation_flags:
            bools.append(flag[0])
        return bools

    def validate(self):
        for tx in self.transactions:
            if not tx.isValid(self.previous_block):
                return False
        # 2. Check if previous
        if self.previous_block == None:
            if self.blockHash == self.computeHash():
                return True
            else:
                return False
        else:
            current_block_validity = self.blockHash == self.computeHash()
            previous_block_validity = self.previous_block.validate()
            return current_block_validity and previous_block_validity

    def mine(self, verbose):
        zeroes = '0'*self.leading_zeros
        difficulty = 16
        flag = True
        start_time = time.time()

        while flag:
            new_hash = self.computeHash()

            if verbose:
                print(new_hash)
            if new_hash.startswith(zeroes):
                if ord(new_hash[self.leading_zeros]) < difficulty: # Multiplies time by 2
                    flag = False
                    break
            self.nonce += 1
            if time.time() - start_time > 10 and self.nonce % 500 == 0 and difficulty < 256:
                if verbose:
                    print(f"Decreasing difficulty from {difficulty} to {difficulty+10}")
                difficulty += 20
        self.blockHash = new_hash

    def __str__(self):
        data_str = "\n"
        for tx_i, tx in enumerate(self.transactions):
            out_str = ""
            for i, outs in enumerate(tx.outputs):
                if i > 0:
                    out_str += " & "
                out_str += f"{outs[1]} to {outs[2]}"
            data_str += f"[{tx_i+1}] Transaction [{tx.id}]: Gas fee: {tx.gas_fee} | {tx.inputs[0][1]} from {tx.inputs[0][2]} --> {out_str} \n"
        string =  f"Block [{self.id}]\n{64*'='}\nMined on: {self.time_stamp} by {self.mined_by}"
        string += f"\n{64*'-'}\nData: {data_str}{64*'-'}\n"
        string += f"Nonce: {self.nonce}\n{64*'-'}\nPrevious Block Hash: {self.previous_hash}\n{64*'-'}\nCurrent Block Hash: {self.blockHash}\n"
        string += f"{(64*'-')}\nValidation Flags: "

        # Adds the username of the person that verified the flag if the flag is not None
        for i in range(3):
            if self.validation_flags[i][0] is not None:
                string += f"{str(self.validation_flags[i][0])} by {self.validation_flags[i][1]}"
            else:
                string += f"{str(self.validation_flags[i][0])}"
            if i < 2:
                string += ", "
        string += f"\n{(64*'-')}\n"

        # string += f"{(64*'-')}\nValidation Flags: {str(self.validation_flags[0][0])}, {str(self.validation_flags[1][0])}, {str(self.validation_flags[2][0])}\n{(64*'-')}\n"
        return string