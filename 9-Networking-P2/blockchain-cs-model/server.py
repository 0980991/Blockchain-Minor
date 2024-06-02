import TxBlock
import socket
import pickle

TCP_PORT = 5010
BUFFER_SIZE=1024

def newConnection(ip_addr):
    print(f"IP ADDRESS: {ip_addr}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_addr, TCP_PORT))
    server_socket.listen()
    return server_socket

def recvObj(c_socket):
    new_s, addr = c_socket.accept()
    whole_data = b""
    while True:
        data = new_s.recv(BUFFER_SIZE)
        if not data:
            break
        whole_data += data
    print(str(whole_data))
    data_ = pickle.loads(whole_data)
    return data_