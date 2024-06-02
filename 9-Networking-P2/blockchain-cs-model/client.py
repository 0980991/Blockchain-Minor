import TxBlock
import Transaction
import Signature
import pickle
import socket

TCP_PORT = 5010

def sendObj(ip_addr, obj):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_addr, TCP_PORT))
    data = pickle.dumps(obj)
    client_socket.send(data)
    client_socket.close()
    return False

