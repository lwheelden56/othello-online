# test-client for calls to server

import socket, threading, sys
global s, rxdata, txdata, HOST, PORT

args = len(sys.argv)
if args == 1:
    print("Error: Host and port must be specified")
    exit()

HOST = sys.argv[1]
PORT = int(sys.argv[2])

def rxThread():
    global s, rxdata
    rxdata = s.recv(1024)
    return rxdata

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

txdata = bytes(input('send:'), 'utf-8')
s.sendall(txdata)

print(rxThread().decode())