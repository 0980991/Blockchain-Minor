import DbInterface as dbi
from GCUser import GCUser
from TxPool import TxPool
from GCTx import GCTx
from GCAccounts import GCAccounts

hashed_pw = GCAccounts.hash_string("password123")
joe = GCUser("JOE", hashed_pw)
mark = GCUser("MARK", hashed_pw)
shane = GCUser("SHANE", hashed_pw)


txp = TxPool()
Tx1 = GCTx([("REWARD", 50)], [(joe.pem_public_key, 50)])
Tx2 = GCTx([(joe.pem_public_key, 30)], [(mark.pem_public_key, 30)])
Tx1.sign(joe.private_key)
Tx3 = GCTx([(joe.pem_public_key, 20)], [(shane.pem_public_key, 20)])
Tx1.sign(joe.private_key)

txp.add(Tx1)
txp.add(Tx2)
txp.add(Tx3)
for tx in txp.transactions:
    print(tx)
    # print(f"Tx [{tx.id}]: {tx.inputs[0][0]}: {tx.inputs[0][1]}")

txp.save()
txp.load()


txp.remove(1)

for tx in txp.transactions:
    print(f"Tx [{tx.id}]: {tx.inputs[0][0]}: {tx.inputs[0][1]}")

txp.clear()

for tx in txp.transactions:
    print(f"Tx [{tx.id}]: {tx.inputs[0][0]}: {tx.inputs[0][1]}")

