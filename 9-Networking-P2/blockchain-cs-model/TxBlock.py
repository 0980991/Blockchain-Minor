#!/usr/bin/env python3
"""Transactions -> Ledger (Block Validation): Exercise

The goal of this exercise is to learn how a blockchain for the transactions is implemented.
In this scenario the implementation of the block is extended with a validation function for the block.
Each block contains his own hash value, transaction data and the hash value of previous block.
Check the provided code in both files, Signature.py, Transaction.py and Blockchain.py.
In Blockchain.py the is_valid() method is provided to check the validity of the block,
rebuild the Block module to satisfy our testing scenario.
The testing scenario here covers tempering the data of one block.
This tempering should be detectable.

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code
    * run the test of this exercise located in same folder.

To test run 'TxBlock_t.py' in your command line

Notes:
    * do not change class structure or method signature to not break unit tests
    * Check previous tutorials for more information on this topic
"""
from BlockChain import CBlock
from Signature import generate_keys, sign, verify
from Transaction import Tx
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import random
class TxBlock (CBlock):

    # TODO 1: Initialize the block
    # Each block contains a list for the data and a hash value to previous block
    def __init__(self, previousBlock=None):
        super(type(self), self).__init__([], previousBlock)
        self.data = []
        self.prevBlock = previousBlock
        self.prevHash = None

    # TODO 2: Append the transaction to the data list
    def addTx(self, Tx_in):
        self.data.append(Tx_in)


    # TODO 3: Check the validity of each transaction in the data list
    # and check the validity of other blocks in the chain to make the cchain tamper-proof
    # Expected return value is true or false
    def is_valid(self):
        if not super(type(self), self).is_valid():

            return False
        for tx in self.data:
            if not tx.is_valid():
                return False
        return True

    def mine(self, leading_zeros):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), "utf8"))
        digest.update(bytes(str(self.previousHash), "utf8"))
        flag = False
        nonce = 0
        while not flag:
            # for _ in range(500000):                    # CAN BE any range         # This lenght can differ and should not affect the time it takes to find it.
                # self.nonce = ''.join([chr(random.randint(48, 123)) for _ in range(10*leading_zeros)])

            digest_temp = digest.copy()
            digest_temp.update(bytes(str(nonce), 'utf8'))
            hash = digest_temp.finalize()

            if hash[:leading_zeros] == bytes('0' * leading_zeros, 'utf8'):
                if int(hash[leading_zeros]) < 128: # Multiplies time by 2
                    flag=True
                    self.nonce = nonce
            nonce  += 1
            del digest_temp


        self.blockHash = self.computeHash()
        return

        # if self.previousBlock is not None:
        #     self.previousHash=self.previousBlock.computeHash()
        #     print()
        # zeroes = '0'*leading_zeros
        # flag = True
        # new_hash = ''
        # while flag:
        #     new_hash = self.computeHash()
        #     if new_hash.startswith(zeroes):
        #         flag = False
        #     else:
        #         self.nonce += 1
        # self.blockHash = new_hash

    def __str__(self):
        print(f"Prev Hash: {self.prevHash}\nData: {self.data}\n")
