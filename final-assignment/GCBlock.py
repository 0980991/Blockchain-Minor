import Signature as sig

class GCBlock:
    def __init__(self, data, previousBlock):
        self.data = []
        self.nonce = 0
        self.previousBlock = previousBlock
        if previousBlock != None:
            self.previousHash = previousBlock.computeHash()

    def addTx(self, Tx_in):
        self.data.append(Tx_in)

    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previousHash),'utf8'))
        return digest.finalize()

    def validate(self):
        # 1. Check if tranactions in block are valid
        for tx in self.data:
            if not tx.isValid():
                return False
        # 2. Check if previuos
        if self.previousBlock == None:
            if self.blockHash == self.computeHash():
                return True
            else:
                return False
        else:
            current_block_validity = self.blockHash == self.computeHash()
            previous_block_validity = self.previousBlock.is_valid()
            return current_block_validity and previous_block_validity

    def mine(self, leading_zero):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf-8'))
        digest.update(bytes(str(self.previousHash), 'utf-8'))

        found = False
        nonce = 0
        while not found:
            h = digest.copy()
            h.update(bytes(str(nonce), 'utf-8'))
            hash = h.finalize()
            if hash[:leading_zero] == bytes('0'*leading_zero, 'utf-8'):
                if int(hash[leading_zero]) < timing_variable:
                    found = True
                    self.nonce = nonce
            nonce += 1
            del h
        self.blockHash = self.computeHash()
