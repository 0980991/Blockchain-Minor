import selectors
import socket
import types
import pickle
from TxPool import TxPool
from BlockChain import BlockChain
from DbInterface import DbInterface as dbi

selector = selectors.DefaultSelector()
data = []

def accept_wrapper(sock):
    conn, addr = sock.accept()
    # print(f'Accepted connection from {addr}')
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(conn, events, data=data)

def service_connection(key, mask, user):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(16384)
        if recv_data:
            message = pickle.loads(recv_data)
            response = handle_request(message, user)
            data.outb += pickle.dumps(response)
        else:
            # print(f'Closing connection to {data.addr}')
            selector.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

def handle_request(message, user):
    global data
    try:
        request = message  # Using the unpickled data directly
        txpool = TxPool()
        blockchain = BlockChain()
        if request['type'] == 'transaction_add':
            if request['data'].isValid():
                txpool.add(request['data'])
                txpool.sort()
                txpool.save()
                return 'Success'
            else:
                return 'invalid transaction'
        elif request['type'] == 'transaction_remove':
            if request['data'].isValid():
                txpool.remove(request['data'].id)
                txpool.sort()
                txpool.save()
                return 'Success'
            else:
                return 'invalid transaction'
        elif request['type'] == 'user_add':
            dbi.insertUser(request['data'])
            return 'Success'
        elif request['type'] == 'user_changepw':
            dbi.updatePwHash(request['data']['username'], request['data']['password'])
            return 'Success'
        elif request['type'] == 'block_add':
            blockchain.load()
            blockchain.check_duplicate_and_add(request['data'])
            for transactions in request['data'].transactions:
                txpool.remove(transactions.id)
            txpool.sort()
            txpool.save()
            blockchain.save()
            return 'Success'
        elif request['type'] == 'logged_in':
            if user != None and user.username != None and user.username == request['data']:
                return True
            else:
                return False
        elif request['type'] == 'block_verified':
            blockchain.load()
            current_block = blockchain.latest_block

            while current_block is not None:
                if current_block.id == request['data']["block"].id:
                    break
                current_block = current_block.previous_block

            if current_block is None:
                return f"Block with ID {request['data']['block'].id} not found."

            # Get the username that verified it
            username = request['data']["username"]

            # Check if the username has already validated this block
            for flag in current_block.validation_flags:
                if flag[1] == username:
                    return f"User {username} has already validated this block."

            # Add the validation to the current block
            for i in range(len(current_block.validation_flags)):
                if current_block.validation_flags[i][0] is None:
                    current_block.validation_flags[i] = [True, username]
                    break
            else:
                return f"Block with ID {request['data']['block'].id} already has all validation flags set."

            # Save the updated blockchain
            blockchain.save()
            return "Validation flag added and blockchain saved."
        elif request['type'] == "blockchain_sync":
            blockchain.load()
            return blockchain.latest_block
        else:
            print(f'type {request["type"]} is not recognized')
            print(f'Current data: {data}')
            return f'Failed: type {request["type"]} is not recognized'
        
    except Exception as e:
        print(f'Error handling request: {e}')
        return f'Failed: {str(e)}'

def start_server(app_instance, host='localhost', port=5006):
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen()
    # print(f'Listening on {(host, port)}')
    lsock.setblocking(False)
    selector.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    user = app_instance.user
                    service_connection(key, mask, user)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        selector.close()
