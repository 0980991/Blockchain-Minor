from server import *
SERVER = "localhost"
TCP_PORT = 5010
if __name__ == "__main__":

    server = newConnection(SERVER)
    newB = recvObj(server)

    if newB.is_valid():
        print("Sucess! The block is balid")
    else:
        print("ERROR! Block is invalid")

    if newB.data[0].inputs[0][1] == 1:
        print("Success! The input value matches")
    else:
        print(f"ERROR! The input value is not 1! Instead it is {newB.data[0].inputs[0][1]}")

    if newB.data[0].inputs[1][1] == 1:
        print("Success! The input value matches")
    else:
        print(f"ERROR! The input value is not 1! Instead it is {newB.data[0].inputs[1][1]}")

    if newB.data[1].inputs[0][1] == 2:
        print("Success! The input value matches")
    else:
        print(f"ERROR! The input value is not 1! Instead it is {newB.data[1].inputs[0][1]}")

    if newB.data[1].inputs[1][1] == 1:
        print("Success! The input value matches")
    else:
        print(f"ERROR! The input value is not 1! Instead it is {newB.data[1].inputs[1][1]}")

    newTx = recvObj(server)
    print(newTx)