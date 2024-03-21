from Signature import *
from Transaction import *
import pickle
from cryptography.hazmat.primitives import serialization
if __name__ == '__main__':
    alex_prv, alex_pbc = generate_keys()
    sample_message = b'hello'
    mes_sig = sign(sample_message, alex_prv)
    v_flag = verify(sample_message, mes_sig, alex_pbc)
    if v_flag:
        print("verified!")
    else:
        print("Not Verified!")

    save_handle = open('tx.dat', 'wb')
    pickle.dump(Tx1, save_handle)
    save_handle.close()

    load_handle.open('tx.dat', 'rb')
    loaded_sig = pickle.load(load_handle)

    if .is_valid():
        print("is Valid")
    else:
        print("is not valid")

    v_flag = verify(sample_message, laoded_sig, alex_pbc)
    if v_flag:
        print("verified!")
    else:
        print("Not Verified!")
#     prv_key, pbc_key = keys
#     b_pw = pw.encode('utf-8')
#     prv_key_pem = prv_key.private_bytes(
#         encoding=Encoding.PEM,
#         format=PrivateFormat.PKCS8,
#         encryption_algorithm=serialization.BestAvailableEncryption(b_pw), # You can use a password for encryption if needed
#     )
#     pbc_key_pem = pbc_key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )

#     with open(f"{keys_file_name}.pem", "wb") as f:
#         f.write(prv_key_pem)
#         f.write(pbc_key_pem)