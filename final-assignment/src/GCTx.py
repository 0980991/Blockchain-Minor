import Signature as s
from datetime import datetime as dt
from datetime import timedelta as td
import HelperFunctions as hf
import random as r
import GCAccounts

## FOR DEBUG
import inspect
import os


class GCTx:
    def __init__(self, inputs=None, outputs=None, gas_fee=0.0):
        self.time_stamp = dt.now()
        self.id = self.time_stamp.strftime('%Y%m%d%H%M%S%f')

        # Inputs are structured as [(pem_public_key, amount, username)]
        if inputs is None:
            inputs = []
        self.inputs = inputs
        # Outputs are structured as [(pem_public_key, amount, username), (pem_public_key, amount, username)]

        if outputs is None:
            outputs = []

        self.outputs = outputs
        self.gas_fee = gas_fee
        self.is_valid = False
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

        # string += f"{64*'-'}\nEXTRA REQUIRED SIGNATURES: "
        # if self.reqd == []:
        #         string += "<No Extra Signatures>"
        # else:
        #     for sig in self.reqd:
        #         string += f"{str(sig)}\N"

        string += f"{64*'='}"
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

    def userInOutputs(self, username):
        for output in self.outputs:
            if output[2] == username:
                return True
        return False

    def isValid(self, prev_block=None): # Prev_block is only used for verifying the mining reward sum of the previous block.
        total_in = 0
        total_out = 0
        tx_data = self.collectTxData()

        for addr,amount,user in self.inputs:
            found = False
            # 1. Verify Sender Signatures
            if addr == "REWARD":
                if user == "Signup Reward" and amount == 50.0:
                    #############################
                    log_str = f"{os.path.basename(inspect.stack()[1].filename)}: line {inspect.stack()[1].lineno} | Tx [{self.id}] validated."
                    log_str += f" This TX is a {user}."
                    hf.logEvent(log_str, "log_validation.txt")
                    #############################
                    found = True
                elif user == "Mining Reward" and amount == prev_block.getRewardSum():
                    #############################
                    log_str = f"{os.path.basename(inspect.stack()[1].filename)}: line {inspect.stack()[1].lineno} | Tx [{self.id}] validated."
                    log_str += f" This TX is a {user}."
                    hf.logEvent(log_str, "log_validation.txt")
                    #############################
                    found = True
            else:
                #############################
                log_str = f"{os.path.basename(inspect.stack()[1].filename)}: line {inspect.stack()[1].lineno} | Tx [{self.id}] validated."
                log_str += f" This TX is sent by {user}."
                hf.logEvent(log_str, "log_validation.txt")
                #############################
                for sig in self.sigs:
                    if s.verify(tx_data, sig, s.deserializePublicKey(addr)):
                        found = True
            if not found:
                self.is_valid = False
                hf.enterToContinue("ERROR: The transaction was not signed (correctly) and is not a REWARD transaction.")
                return False

            # 2. Verify input amount
            if amount < 0:
                self.is_valid = False
                hf.enterToContinue("ERROR: The sent amount is less than 0")
                return False
            total_in = total_in + amount

        # for addr in self.reqd:
        #     found = False
        #     for sig in self.sigs:
        #         # 3. Verify required signatures against
        #         if s.verify(tx_data, sig, s.deserializePublicKey(addr)):
        #             found = True
        #     if not found:
        #         self.is_valid = False

        #         return False

        for addr,amount,username in self.outputs:
            # 4. Verify the output amount is greater than 0
            if amount < 0:
                self.is_valid = False
                hf.enterToContinue("ERROR: The received amount is less than 0")
                return False
            total_out = total_out + amount

        # 5. Verify input is greater the output
        if total_out > total_in:
            self.is_valid = False
            hf.enterToContinue("ERROR: The sum of outputs is greater than the sum of inputs!")

            return False
        self.is_valid = True
        return True
