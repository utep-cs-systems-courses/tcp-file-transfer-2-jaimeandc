#! /usr/bin/env python3

import sys
sys.path.append("../lib") # For params
import re, socket, params

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
listsock.listen(1)
print("Listening on:", bindAddr)
print("Waiting for connection...")

conn, addr = listsock.accept()

print(addr, "is connected to server.")

from framedSock import framedSend, framedReceive
file = open("ServerFiles.txt","w") ## open file where data from client files will be saved
files_received = []
while True:
    filename = framedReceive(conn, debug)## Server waits for file name
    if filename in files_received:## Check if server already recived file
        print("%s already exists" % filename)
        break
    else:
        files_received.append(filename)## add filename to files_received
        file.write("Contents of '%s'\n" % filename)## write name of file to outfile
        payload = framedReceive(conn, debug) ## save payload from file
        if debug: print("receving:", payload)
        if not payload:
            print("Done saving data from files and client disconected")
            break
        #print("What was read from '%s': %s\n" % (payload, filename))
        while payload.decode("utf-8") != "exit":
            file.write(payload.decode("utf-8"))
            framedSend(conn,payload,debug)
            payload = framedReceive(conn,debug)

print("Server Wrote the following files to ServerFiles.txt")
for x in files_received:
    print(x)
file.close()
listsock.close()
