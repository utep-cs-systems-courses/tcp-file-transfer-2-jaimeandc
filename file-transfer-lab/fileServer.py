#! /usr/bin/env python3
import sys
sys.path.append("../lib") # For params
import re, socket, params, os
from os.path import exists
from os.path import join as pjoin

from framedSock import framedSend, framedReceive
true = "True"
false = "False"
switchesVarDefaults= (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False),
    )
progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

listsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
listsock.bind(bindAddr)
listsock.listen(3)
print("Listening on:", bindAddr)
received_files = []
with open("test.txt", "wb")as file2:
    while True:
        conn, addr = listsock.accept()
        print("Incoming connection from ", addr)
        if not os.fork():
            while True:
                filename = framedReceive(conn,debug)
                if filename in received_files:
                    framedSend(conn,b"True",debug) ## send message to client that file is duplicate
                else:## if new file
                    framedSend(conn,b"False", debug)
                    try:
                        payload = framedReceive(conn,debug) ## receive file contents
                        if not payload:
                            print("Done")
                            break
                        #with open("test.txt", "wb") as file2:
                        #    file2.write(payload)
                        file2.write(payload)
                    except:
                        print("Connection to Client was lost 1")
                        break
                    try:
                        framedSend(conn,str.encode("Server wrote file"),debug)
                    except:
                        print("Connection to client was lost...")
                        break
