import Signature as s
from datetime import datetime as dt
from datetime import timedelta as td
import random as r
import GCAccounts

class GCTx:
    # TODO : ID resets when program resets. It should continue from te last ID
    def __init__(self, inputs=None, outputs=None, gas_fee=0.0):
        self.time_stamp = dt.now()
        self.id = self.time_stamp.strftime('%Y%m%d%H%M%S%f')[4:]

        # Inputs are structured as [(pem_public_key, amount, username)]
        if inputs is None:
            inputs = []
        self.inputs = inputs
        # Outputs are structured as [(pem_public_key, amount, username), (pem_public_key, amount, username)]
        
        if outputs is None:
            outputs = []

        self.outputs = outputs
        self.gas_fee = gas_fee
        self.sigs = []
        self.reqd = []

    def __str__(self):
        string = f"{60*'='}\nTransaction ID: {self.id}\n{64*'-'}\nINPUTS: "
        for inp in self.inputs:
            # username = GCAccounts.idPublicKey(inp[0])
            string += f"{str(inp[1])} from {inp[2]}\n"
        string += f"{64*'-'}\nOUTPUTS: "
        for out in self.outputs:
            # username = GCAccounts.usernameFromPublicKey(out[0])
            string += f"{str(out[1])} to {out[2]}\n"
        string += f"{64*'-'}\nGAS FEE: {self.gas_fee}\n"
        string += f"{64*'-'}\nSIGNATURES: "
        if self.sigs == []:
            string += "<This transaction is not signed by the sender>\n"
        for sig in self.sigs:
            string += f"{str(sig)}\n"
        string += f"{64*'-'}\nEXTRA REQUIRED SIGNATURES: "
        if self.reqd == []:
                string += "<No Extra Signatures>"
        else:
            for sig in self.reqd:
                string += f"{str(sig)}"

        string += f"\n{64*'='}"
        return string

    def addInput(self, from_addr, amount):
        self.inputs.append((from_addr, amount))

    def addOutput(self, to_addr, amount):
        self.outputs.append((to_addr, amount))

    def addReqd(self, sig):
        self.reqd.append(sig)

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

        for addr,amount,user in self.inputs:
            found = False
            # 1. Verify Sender Signatures
            for sig in self.sigs:
                if s.verify(tx_data, sig, s.deserializePublicKey(addr)):
                    found = True
            if not found:
                return False

            # 2. Verify input amount
            if amount < 0:
                return False
            total_in = total_in + amount

        for addr in self.reqd:
            found = False
            for sig in self.sigs:
                # 3. Verify required signatures against
                if s.verify(tx_data, sig, s.deserializePublicKey(addr)):
                    found = True
            if not found:
                return False

        for addr,amount,username in self.outputs:
            # 4. Verify the output amount is greater than 0
            if amount < 0:
                return False
            total_out = total_out + amount

        # 5. Verify input is greater the output
        if total_out > total_in:
            return False
        return True
