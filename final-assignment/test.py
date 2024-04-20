import DbInterface as dbi
from GCUser import GCUser
from TxPool import TxPool
from GCTx import GCTx
from GCAccounts import GCAccounts
import HelperFunctions as hf

from GCBlock import GCBlock
from Signature import *
import pickle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend




if __name__ == "__main__":
    hashed_pw = GCAccounts.hash_string("password123")
    joe = GCUser("JOE", hashed_pw)
    mark = GCUser("MARK", hashed_pw)
    shane = GCUser("SHANE", hashed_pw)
    ari = GCUser("ARI", hashed_pw)

    # Valid Blocks
    ####################


    txp = TxPool()
    
    # Create 2 valid transactions Tx1 and Tx2
    Tx1 = GCTx([(joe.pem_public_key, 4)], [(mark.pem_public_key, 1)], 3)
    Tx1.sign(joe.private_key)


    Tx2 = GCTx([(shane.pem_public_key,12)], [(mark.pem_public_key, 2)], 10)
    Tx2.sign(shane.private_key)

    # Add Tx1 and Tx2 to the first block (genesis block)
    b1_txs = [Tx1, Tx2]
    root = GCBlock(b1_txs)
    check2 = root.validate()

    # Create 2 more valid transactions Tx3 and Tx4
    Tx3 = GCTx([(mark.pem_public_key,2)], [(joe.pem_public_key, 1)], 1)
    Tx3.sign(mark.private_key)

    Tx4 = GCTx([(shane.pem_public_key,4)],[(ari.pem_public_key, 1)], 3)
    Tx4.addReqd(mark.pem_public_key)
    Tx4.sign(shane.private_key)
    Tx4.sign(mark.private_key)

    Tx5 = GCTx([("REWARD"), 50], [(joe.pem_public_key, 50)])

    txp.add(Tx1)
    txp.add(Tx2)
    txp.add(Tx3)
    txp.add(Tx4)
    txp.add(Tx5)
    txp.sort()
    

    # Add Tx3 and Tx4 to the second block (the child of the genesis block)
    B1 = GCBlock([Tx3, Tx4], root)

    # if root.validate():
    #     print("Congrats! The genesis block is valid")
    # else:
    #     print("Fail! The genesis block is INVALID")
    if B1.validate():
        print("Congrats! Block 1 is valid")
    else:
        print("Fail! B1 is INVALID")
        

    ### NOTE: Genesis and B1 are seen as valid. I have not tried to alter the data of a block to see if it remains valid (which is wrong)
    ######### I am also not sure if they should be valid since they are not mined but prevBlock.blockHash  must be equal to currBlock.prevHash()

    # Save the block B1 on the disk
    savefile = open("block.dat", "wb")
    pickle.dump(B1, savefile)
    savefile.close()

    # Create new valid transaction Tx5
    Tx5 = GCTx()
    Tx5.addInput(mark.pem_public_key, 2.3)
    Tx5.addOutput(shane.pem_public_key, 2.3)
    Tx5.sign(mark.private_key)
    # Create a new block (a child of the block B1), and the transaction Tx5 to the block
    B2 = GCBlock(B1)
    B2.addTx(Tx5)

    # Load the block B1 from the disk
    loadfile = open("block.dat" ,"rb")
    load_B1 = pickle.load(loadfile)
    loadfile.close()

    for b in [root, B1, B2, load_B1]:
        if b.is_valid():
            print ("Success! Valid block is verified.")
        else:
            print ("Error! Valid block is not verified.")

    # Invalid Blocks
    ######################
    # Creat an invalid transaction Tx6
    Tx6 = GCTx()
    Tx6.addInput(ari.pem_public_key, 2.0)
    Tx6.addOutput(mark.pem_public_key, 15.3)
    Tx6.sign(ari.private_key)
    B3 = GCBlock(B2)
    B3.addTx(Tx6)

    # Creat an invalid transaction Tx7
    Tx7 = GCTx()
    Tx7.addInput(mark.pem_public_key, 2.3)
    Tx7.addOutput(shane.pem_public_key, 2.3)
    Tx7.sign(shane.private_key)
    B4 = GCBlock(B3)
    B4.addTx(Tx7)

    # Creat an invalid transaction Tx8
    Tx8 = GCTx()
    Tx8.addInput(shane.pem_public_key, 0.9)
    Tx8.addOutput(ari.pem_public_key, 0.8)
    Tx8.addReqd(mark.pem_public_key)
    Tx8.sign(shane.private_key)
    B5 = GCBlock(B4)
    B5.addTx(Tx8)

    # Tamper the block before B1 by adding a valid transaction to it
    # This will make the block B1 (the block after the tampered block) invlaid
    B1.previousBlock.addTx(Tx4)

    for b in [B1, B3, B4, B5]:
        if b.is_valid():
            print("Error! Invalid block is verified.")
        else:
            print("Success! Invalid blocks is detected.")

    print('Tx4\n', Tx4)
    print('Tx5\n', Tx5)
# try:
#     fh = open("TxPool.dat", 'rb')
#     transactions = pickle.load(fh)
#     fh.close()
# except FileNotFoundError:
#     if hf.yesNoInput("Error! TxPool.dat could not be located. Make sure it is stored in the same directory as the goodchain.py file\nWould you like to create a new emtpy file?")
#         print("HI")



# txp = TxPool()
# Tx1 = GCTx([("REWARD", 50)], [(joe.pem_public_key, 50)])
# Tx2 = GCTx([(joe.pem_public_key, 30)], [(mark.pem_public_key, 30)])
# Tx1.sign(joe.private_key)
# Tx3 = GCTx([(joe.pem_public_key, 20)], [(shane.pem_public_key, 20)])
# Tx1.sign(joe.private_key)

# txp.add(Tx1)
# txp.add(Tx2)
# txp.add(Tx3)
# for tx in txp.transactions:
#     print(tx)
#     # print(f"Tx [{tx.id}]: {tx.inputs[0][0]}: {tx.inputs[0][1]}")

# txp.save()
# txp.load()


# txp.remove(1)

# for tx in txp.transactions:
#     print(f"Tx [{tx.id}]: {tx.inputs[0][0]}: {tx.inputs[0][1]}")

# txp.clear()

# for tx in txp.transactions:
#     print(f"Tx [{tx.id}]: {tx.inputs[0][0]}: {tx.inputs[0][1]}")

