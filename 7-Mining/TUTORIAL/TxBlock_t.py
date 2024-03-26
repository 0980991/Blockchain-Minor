from TxBlock import TxBlock
from BlockChain import CBlock
from Signature import generate_keys, sign, verify, serialize_keys
from Transaction import Tx

import pickle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from TxBlock import *

leading_zero = 2
timing_var = 128

if __name__ == "__main__":
    alex_prv1, alex_pbc1 = generate_keys()
    mike_prv1, mike_pbc1 = generate_keys()
    rose_prv1, rose_pbc1 = generate_keys()
    mara_prv1, mara_pbc1 = generate_keys()
    alex_prv, alex_pbc = serialize_keys(alex_prv1, alex_pbc1)
    mike_prv, mike_pbc = serialize_keys(mike_prv1, mike_pbc1)
    rose_prv, rose_pbc = serialize_keys(rose_prv1, rose_pbc1)
    mara_prv, mara_pbc = serialize_keys(mara_prv1, mara_pbc1)

    Tx1 = Tx()
    Tx1.add_input(alex_pbc, 6)
    Tx1.add_output(mike_pbc, 5)
    Tx1.sign(alex_prv1)

    Tx2 = Tx()
    Tx2.add_input(rose_pbc, 10)
    Tx2.add_output(alex_pbc, 5)
    Tx2.add_output(mike_pbc, 4)
    Tx2.sign(rose_prv1)


    genesis_block = TxBlock()
    genesis_block.addTx(Tx1)
    genesis_block.addTx(Tx2)
    genesis_block.mine(leading_zero)

    Tx3 = Tx()
    Tx3.add_input(mara_pbc, 11)
    Tx3.add_output(rose_pbc, 5)
    Tx3.add_output(mike_pbc, 5)
    Tx3.sign(mara_prv1)

    Tx4 = Tx()
    Tx4.add_input(alex_pbc, 1)
    Tx4.add_input(rose_pbc, 1)
    Tx4.add_output(mike_pbc, 2)
    Tx4.sign(alex_prv1)
    Tx4.sign(rose_prv1)

    TxB1 = TxBlock(genesis_block)
    TxB1.addTx(Tx3)
    TxB1.addTx(Tx4)
    TxB1.mine(leading_zero)

    fh = open('blockchain.dat', 'wb')
    pickle.dump(TxB1, fh)
    fh.close()

    fh =open('blockchain.dat', 'rb')
    TxB1_loaded = pickle.load(fh)
    fh.close()

    for block in [genesis_block, TxB1, TxB1_loaded, TxB1_loaded.previousBlock]:
        if block.is_valid():
            print("True, is valid")
        else:
            print("False, not valid")


    Tx5 = Tx()
    Tx5.add_input(alex_pbc, 1)
    Tx5.add_input(rose_pbc, 1)
    Tx5.add_output(mike_pbc, 7)
    Tx5.sign(alex_prv1)
    Tx5.sign(rose_prv1)

    Tx6 = Tx()
    Tx6.add_input(alex_pbc, 1)
    Tx6.add_input(rose_pbc, 1)
    Tx6.add_output(mike_pbc, 2)
    Tx6.sign(rose_prv1)

    TxB2 = TxBlock(TxB1)
    TxB2.addTx(Tx5)
    TxB2.addTx(Tx6)
    TxB2.mine(leading_zero)

    for block in [TxB1, TxB2]:
        if block.is_valid():
            print("Fail! The block should be invalid")
        else:
            print("Success! The block is indeed invalid")
