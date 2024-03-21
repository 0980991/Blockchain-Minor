#NOTES: The first check they should not match
#!/usr/bin/env python3
"""Block Integrity -> Tamper Proof Chain: Homework

The goal of this homework is to extend the behavior of a block to created a chain and securely link
them together using cryptography. In general, each block is used to hold a batch of transactions. In addition a cryptographic
hash of the previous block in the chain and some other needed values for computation.
In this homework each block will hold:
    * a string message (data)
    * its own block hash value
    * hash value of the previous block
    * nonce value which will be incremented when a block is mined

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code
    * run the test of this exercise located in same folder.

To test run 'Blockchain_t.py' in your command line

Notes:
    * do not change class structure or method signature to not break unit tests
    * visit this url for more information on this topic:
    https://cryptography.io/en/latest/hazmat/primitives/cryptographic-hashes/
"""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from pyblake2 import blake2b
class CBlock:
    # TODO 1: Initialize the values of a block
    # Make sure you distinguish between the genesis block and other blocks
    def __init__(self, data, previousBlock):
        self.previousHash = None
        self.blockHash = None
        self.data = data
        self.previousBlock = previousBlock
        self.nonce = 0
        if self.previousBlock:
            self.previousHash = self.previousBlock.computeHash()


    # TODO 2: Compute the cryptographic hash of the current block.
    # Be sure which values must be considered to compute the hash properly.
    # return the digest value
    def computeHash(self):
        block_str = str(self.data) + str(self.previousHash) + str(self.nonce)
        digest = blake2b(digest_size=32)
        digest.update(block_str.encode("utf-8"))
        hashed_block = digest.hexdigest()
        return hashed_block

    # TODO 3: Mine the current value of a block
    # Calculates a digest based on required values from the block, such as:
    # data, previousHash, nonce
    # Make sure to compute the hash value of the current block and store it properly
    def mine(self, leading_zeros):
        if self.previousBlock is not None:
            self.previousHash=self.previousBlock.computeHash()
            print()
        zeroes = '0'*leading_zeros
        flag = True
        new_hash = ''
        while flag:
            new_hash = self.computeHash()
            if new_hash.startswith(zeroes):
                flag = False
            else:
                self.nonce += 1
        self.blockHash = new_hash

    # TODO 4: Check if the current block contains valid hash digest values
    # Make sure to distinguish between the genesis block and other blocks
    # Make sure to compare both hash digest values:
    # The computed digest of the current block
    # The stored digest of the previous block
    # return the result of all comparisons as a boolean value
    def is_valid_hash(self):
        # Check if Genesis Block
        if self.previousBlock is None:
            return self.blockHash == self.computeHash()
        current_block_validity = self.blockHash == self.computeHash()
        compute_hash = self.computeHash()
        prev_block_validity = self.previousBlock.computeHash() == self.previousHash
        return current_block_validity and prev_block_validity

