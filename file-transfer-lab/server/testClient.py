#! /usr/bin/env python3

import socket, sys, re
sys.path.append("../../lib")
import params
from os import path
from os.path import exists

from encapFramedSock import EncapFramedSock

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

progname = "testClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Cant parse Server: port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

sock = socket.socket(addrFamily, socktype)

if sock is None:
    print('could not open socket')
    sys.exit(1)
sock.connect(addrPort)

fsock = EncapFramedSock((sock, addrPort))
for i in range(1):
    filename = input("Enter filename: ")
#    file = open(filename,'rb')
#    payload = file.read()
    
#    fsock.send(payload,debug)
#    print("SERVER SAYS: ", fsock.receive(debug).decode())
    if exists(filename):
        file = open(filename,'rb')
        payload = file.read()
        if len(payload) == 0:
            print("Cant send empty file")
            sys.exit(0)
        else:
            fsock.send(filename.encode(), debug) ## send filename to check for existance
            file_exists = fsock.receive(debug).decode()
            if file_exists == 'True':
                print("That file exits all ready")
                sys.exit(0)
            elif file_exists == 'exists': ##
                print("Someones already writing this to the server. Try again later") ##
                sys.exit(0)
            else:
                fsock.send(payload,debug)
                print("Server says:  ", fsock.receive(debug).decode())
    else:
        print("File '%s' dosnt exist." % filename)
    
    ##fsock.send(test.encode(),debug)
    ##print("Got your message: %s" % fsock.receive(debug).decode())
    #print("sending hello world")
    #fsock.send(b"helloworld", debug)
    #print("received:", fsock.receive(debug))
