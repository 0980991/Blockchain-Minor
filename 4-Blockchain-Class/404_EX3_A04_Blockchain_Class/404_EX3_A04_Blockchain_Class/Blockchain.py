#!/usr/bin/env python3
"""Block Integrity -> Blockchain Data Structure: Exercise 1

The goal of this exercise is to learn how a simple blockchain can be created and securely linked
together using cryptography. In general, each block is used to hold a batch of transactions. In addition a cryptographic
hash of the previous block in the chain and some other needed values for computation.
For the simplicity of this exercise each block will hold a string message (data) and hash of the previous block (previousBlock).
The computeHash() method should compute the cryptographic hash of the current block.
Be sure which values must be considered to compute the hash properly.

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
    previousHash = None
    previousBlock = None
    data = None

    # TODO 1: Initialize a block
    # Make sure you initialize the genesis block and transaction blocks differently
    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        if self.previousBlock is not None:
            self.previousHash = self.previousBlock.computeHash()

    # TODO 2: Compute the hash of a the current block
    # Make sure you include all required data
    def computeHash(self):
        block_str = str(self.data) + str(self.previousHash)
        digest = blake2b(digest_size=32)
        digest.update(block_str.encode("utf-8"))
        hashed_block = digest.hexdigest()
        return hashed_block