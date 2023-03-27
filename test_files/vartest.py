import time, socket, threading
global s, rxdata, txdata, clients, clientS1, clientS2

host = ''
port = 8002
clients=[]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(2)
# s as a server socket should not be referenced after this

def accept_clients():
    global s, clients
    while len(clients)<=1:
        clientsocket, addr = s.accept()
        print('Connected to: ' + addr[0] + ':' + str(addr[1]))
        clientsocket.sendall(bytes("Connected",'utf-8'))
        threading.Thread(target=client_acc_thread, args=(clientsocket,)).start()
    return

def client_acc_thread(client):
    global s, clients
    if len(clients)==1:
        clientS2=client
        clients.append(clientS2)
        clientS2.sendall(bytes("black", 'utf-8'))
    if len(clients)==0:
        clientS1=client
        clients.append(clientS1)
        clientS1.sendall(bytes("white", 'utf-8'))
    if len(clients)>1:
        client.sendall(bytes("full", 'utf-8'))
        client.close()
#    for c in range(0, len(clients)):
#        clients[c].sendall(bytes("gameon", 'utf-8'))
    return

accept_clients()

# note : good to test , need client reprogramming