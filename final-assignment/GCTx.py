import itertools
import Signature as s

class GCTx:
    id_obj = itertools.count()
    def __init__(self, inputs=None, outputs=None):
        self.id = next(GCTx.id_obj)
        self.inputs = inputs
        self.outputs = outputs
        self.sigs = []
        self.reqd = []

    def __str__(self):
        string = "INPUTS:\n"
        for inp in self.inputs: 
            # username = GCAccounts.idPublicKey(inp[0])
            string += f"{str(inp[1])} from {inp[0]}\n"
        string += "OUTPUTS:\n"
        for out in self.outputs:
            # username = GCAccounts.idPublicKey(out[0])
            string += f"{str(out[1])} to {out[0]}\n"
        string += "EXTRA REQUIRED SIGNATURES:\n"
        for sig in self.reqd:
            string += f"{str(sig)}"
        string += "SIGNATURES:\n"
        for sig in self.sigs:
            string += f"{str(sig)}\n"
        string += "END\n"
        return string

    def addInput(self, from_addr, amount):
        self.inputs.append((from_addr, amount))

    def addOutput(self, to_addr, amount):
        self.outputs.append((to_addr, amount))

    def addReqd(self, sig):
        self.reqd.append(sig)

    def collect_transaction_data(self):
        tx_data=[]
        tx_data.append(self.inputs)
        tx_data.append(self.outputs)
        tx_data.append(self.reqd)
        return str(tx_data).encode('utf-8')

    def sign(self, private_key):
        message = self.collectTxData()
        newsig = s.sign(message, private_key)
        self.sigs.append(newsig)

    def collectTxData(self):
        tx_data = []
        tx_data.append(self.inputs)
        tx_data.append(self.outputs)
        tx_data.append(self.reqd)
        return tx_data

    def isValid(self):
        total_in = 0
        total_out = 0
        tx_data = self.collectTxData()

        for addr,amount in self.inputs:
            found = False
            # 1. Verify Sender Signatures
            for s in self.sigs:
                if verify(tx_data, s, addr):
                    found = True
            if not found:
                return False

            # 2. Verify input amount
            if amount < 0:
                return False
            total_in = total_in + amount

        for addr in self.reqd:
            found = False
            for s in self.sigs:
                # 3. Verify required signatures against
                if verify(tx_data, s, addr):
                    found = True
            if not found:
                return False

        for addr,amount in self.outputs:
            # 4. Verify the output amount is greater than 0
            if amount < 0:
                return False
            total_out = total_out + amount

        # 5. Verify input is greater the output
        if total_out > total_in:
            return False
        return True
