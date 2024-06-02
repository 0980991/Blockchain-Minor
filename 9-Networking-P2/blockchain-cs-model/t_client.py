import TxBlock
from Signature import *
from Transaction import *
from BlockChain import *
from client import *

SERVER = "localhost"
TCP_PORT = 5010

if __name__ == "__main__":

    keys_list =[]

    alex_prv, alex_pbc = generate_keys()
    keys_list.append(('alex', alex_prv, alex_pbc))

    mike_prv, mike_pbc = generate_keys()
    keys_list.append(('mike', mike_prv, mike_pbc))

    rose_prv, rose_pbc = generate_keys()
    keys_list.append(('rose', rose_prv, rose_pbc))

    mara_prv, mara_pbc = generate_keys()
    keys_list.append(('mara', mara_prv, mara_pbc))

    mara_prv_s, mara_pbc_s = serialize_keys(mara_prv, mara_pbc)
    alex_prv_s, alex_pbc_s = serialize_keys(alex_prv, alex_pbc)
    rose_prv_s, rose_pbc_s = serialize_keys(rose_prv, rose_pbc)


    # --------------------------------------
    Tx1 = Tx()
    Tx1.add_input(alex_pbc, 2.3)
    Tx1.add_output(mike_pbc, 1.0)
    Tx1.add_output(mike_pbc, 1.1)
    Tx1.sign(alex_prv_s)
   
    # --------------------------------------
    Tx2 = Tx()
    Tx2.add_input(alex_pbc, 2.2)
    Tx2.add_input(mike_pbc, 1.0)
    Tx2.add_output(rose_pbc, 1.1)
    Tx2.sign(alex_prv_s)

    # --------------------------------------
    Tx3 = Tx()
    Tx3.add_input(rose_pbc, 1.2)
    Tx3.add_output(alex_pbc, 1.1)
    Tx3.sign(rose_prv_s)
    Tx3.sign(mara_prv_s)

    # --------------------------------------
B1 = TxBlock.TxBlock(None)
B1.addTx(Tx1)
B1.addTx(Tx2)

sendObj(SERVER, B1)
sendObj(SERVER, Tx2)