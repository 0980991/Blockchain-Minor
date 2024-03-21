from Signature import *
from Transaction import *
import pickle


if __name__ == '__main__':
    alex_prv, alex_pbc = generate_keys()
    mike_prv, mike_pbc = generate_keys()
    rose_prv, rose_pbc = generate_keys()
    mara_prv, mara_pbc = generate_keys()



    Tx1 = Tx()
    Tx1.add_input(alex_pbc, 1)
    Tx1.add_output(mike_pbc, 1)
    Tx1.sign(alex_prv)

    if Tx1.is_valid:
        print("is Valid")
    else:
        print("is not valid")
# BEFORE USING PICKLE WE MUST SERIALIZE THE KEYS/ seriliaziation larbary else you should get:
# Exception has occurred: TypeError
# can't pickle _cffi_backend.FFI objects
# THIS IS IMPLEMENTED IN HE GENERATE KEYS class

    save_handle = open('tx.dat', 'wb')
    pickle.dump(Tx1, save_handle)
    save_handle.close()

    load_handle.open('tx.dat', 'rb')
    loaded_tx = pickle.load(load_handle)

    if loaded_tx.is_valid():
        print("is Valid")
    else:
        print("is not valid")


