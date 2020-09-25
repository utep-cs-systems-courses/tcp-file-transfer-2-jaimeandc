#! /usr/bin/env python3

import socket, sys, re
import os.path
from os import path

sys.path.append("../lib") # For params
import params

from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), #boolean (set if present)
    (('-?', '--usage'), "usage", False), #boolean (set if present)
    )

progname = "fileClient" 
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print("Could not open socket...")
    sys.exit(1)

s.connect(addrPort)
sentFiles = []
files = ["testfile.txt", "file1.txt", "file2.txt", "file3.txt"]


for file in files:
    #while not path.exists(file): ##Check if file exist
    #    print("Sorry could not file '%s'" % file)
    #    f.close()
    #    pass
    if file in sentFiles: ## check if file has already been sent
        print("Tried sending '%s' but it already exist in the server." % file)
        
    else:
        print("Sending File %s to Server:" % file)
        framedSend(s, str.encode(file),debug)
        sentFiles.append(file) ## add filename to sentFile list
        with open(file, "r") as f:
            if os.stat(file).st_size == 0: ## check if file is empty
                print('%s is empty file\n' % file)
                f.close()
            else:
                for line in f:
                    framedSend(s, str.encode(line),debug)
                    print("Server Received: ",framedReceive(s,debug))
                print("Server Coppied: '%s'\n" % file)
                f.close()            
s.close() ## no more files to send close socket.
        
