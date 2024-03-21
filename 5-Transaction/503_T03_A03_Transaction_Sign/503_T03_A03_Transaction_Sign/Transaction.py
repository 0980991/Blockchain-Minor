#!/usr/bin/env python3
"""
Transaction Class - Definition of Input and Output

This is just a copy of the previous tutorial. If you have already completed the previous tutorial,
simply copy and paste the code of transaction class, here.

Check the test file. It includes signing and verification of transactions
using this new defined transaction class.
"""

from Signature import *


class Tx:

    # TODO 1: Complete the method
    # In this method, you should initialize the variables for inputs and ouputs
    # of a transaction.
    # Inputs and Ouputs should be defined as list, where a list of senders (and the sending amount),
    # and a list of receivers (and the receiving amount) are stored.
    def __init__(self):
        self.inputs = []
        self.outputs = []

    # TODO 2: Complete the method
    # This method should add a new sender and the associated amount to the list of inputs
    # An input is a list of senders (from_addr) and the amount sent by each sender (amount)
    def add_input(self, from_addr, amount):
        self.inputs.append([from_addr, amount])

    # TODO 3: Complete the method
    # This method should add a new receiver and the associated amount to the list of outputs
    # An output is a list of receivers (to_addr) and the amount recived by each receiver (amount)
    def add_output(self, to_addr, amount):
        self.outputs.append([to_addr, amount])