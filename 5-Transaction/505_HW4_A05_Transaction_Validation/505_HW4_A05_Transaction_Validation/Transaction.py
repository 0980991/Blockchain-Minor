#!/usr/bin/env python3
from Signature import *
"""
Transaction Class

The goal of this exercise is to learn how to complete transaction class.
A transaction is composed of a list of Inputs and a list of outputs, and few methods.
add_input() and add_output(), and sign() are already completed in the previous tutorials and exercise.
In this hoemwork, we will add another method is_valid() to the class. With this method, we can
validate a transaction.

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code
    * run the test of this tutorial located in same folder.

To test run 'Transactions_t.py' in your command line

Notes:
    * do not change class structure or method signature to not break unit tests
"""
class Tx:
    inputs = None
    outputs =None
    sigs = None
    reqd = None

    # TODO 1: Complete the method
    # These three methods are already done in the previous tutorials
    # you can copy and paste the previous codes here
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []

    def add_input(self, from_addr, amount):
        self.inputs.append([from_addr, amount])

    def add_output(self, to_addr, amount):
        self.outputs.append([to_addr, amount])

    # TODO 2: Complete the method
    # We would like to have another method to add extra required signature if needded (e.g. escrow)
    # with this method, we can specify other required signature to the transaction by adding the
    # public key of the required signature
    # If this signature is needed, later we can check if the transaction is also signed by that person/party.
    def add_reqd(self, addr):
        self.reqd.append(addr)

    def collect_transaction_data(self):
        tx_data=[]
        tx_data.append(self.inputs)
        tx_data.append(self.outputs)
        tx_data.append(self.reqd)
        return str(tx_data).encode('utf-8')

    # TODO 3: Complete the method
    # This method is also already done in the previous tutorials.
    # you can copy and paste the previous codes here
    def sign(self, private):
        message = self.collect_transaction_data()
        sig = sign(message, private)
        self.sigs.append(sig)


    # TODO 4: Complete the method
    # This method is used to validate a transaction.
    # To validate a transaction, we must check few important things:
    #   1 -  Every entery in inputs need to be signed by the relevant sender, and
    #   2 -  If an extra required signature is needed, the signature need to be verified too, and
    #   3 -  The total amount of outputs must not exceed the total amount of inputs.
    def is_valid(self):
        total_in = 0
        total_out = 0
        message = []
        message = self.collect_transaction_data()
        for from_addr, amount in self.inputs:
            flag = False
            for s in self.sigs:
                if verify(message, s, from_addr):
                    flag = True
            if not flag:
                return False
            if amount < 0:
                return False
            total_in += amount
        for addr in self.reqd:
            flag = False
            for s in self.sigs:
                if verify(message, s, addr):
                    flag = True
            if not flag:
                return False
        for to_addr, amount in self.outputs:
            if amount < 0:
                return False
            total_out += amount
        if total_out > total_in:
            return False
        return True
