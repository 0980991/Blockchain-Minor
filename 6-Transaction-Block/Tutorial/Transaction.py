#!/usr/bin/env python3
"""
Transaction Class

The goal of this exercise is to learn how to complete transaction class.
A transaction is composed of a list of Inputs and a list of outputs, and few methods.
add_input and add_output are already completed in the previous tutorials.
In this exercise, we will add a sign method to the class. With this method, we can
sign a transaction.

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code
    * run the test of this tutorial located in same folder.

To test run 'Transactions_t.py' in your command line

Notes:
    * do not change class structure or method signature to not break unit tests
"""

from Signature import *

class Tx:

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []      # A placeholder for any other extra required signature (e.g. escrow)


    # TODO 1: Complete the method
    # These two methods are already done in the previous tutorials
    # you can copy and paste the previous codes here
    def add_input(self, from_addr, amount):
        self.inputs.append([from_addr, amount])

    def add_output(self, to_addr, amount):
        self.outputs.append([to_addr, amount])


    def collect_transaction_data(self):
        tx_data=[]
        tx_data.append(self.inputs)
        tx_data.append(self.outputs)
        tx_data.append(self.reqd)
        # data = ""
        #     data += str(inp[0]) + " " + str(inp[1]) + "\n"
        # for out in self.outputs:
        #     data += str(out[0]) + " " + str(out[1]) + "\n"
        return str(tx_data)

    # TODO 2: Complete the method
    # In this method:
    #   1 - You should collect all data of the transaction, and then
    #   2 - Sign data and add it to the variable sigs
    #
    # It is good idea to create a seperate private or protected method to collect all data of
    # transaction before signing it.
    def sign(self, private):
        data_str=self.collect_transaction_data()
        b_data = data_str.encode('utf-8')
        self.sigs.append(sign(b_data, private))
        print("deze klopt")

    def is_valid(self):
        total_in = 0
        total_out = 0
        message = self.collect_transaction_data()
        for addr, amount in self.inputs:
            found = False
            for s in self.sigs:
                if verify(message, s, addr):
                    found = True
                if not found:
                    return False
                if amount < 0:
                    return False

        for addr in self.reqd:
            found = False
            for s in self.sigs:
                if verify(message, s, addr):
                    found = True
                if not found:
                    return False

        for addr, amount in self.ouputs:
            if amount > 0:
                return False
            total_out = total_out + amount

        if total_out > total_in:
            return False
        return True