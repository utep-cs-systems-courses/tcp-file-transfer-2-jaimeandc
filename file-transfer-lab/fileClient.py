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

progname = "framedClient" 
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
files = ["testfile.txt", "file1.txt", "emptyfile.txt", "file2.txt", "file3.txt", "file3.txt", "nonexistentFile.txt"]

def is_empty_file(filename):
    return os.path.isfile(filename) and os.path.getsize(filename) > 0

for file in files:
    if is_empty_file(file) == False:
        print("'%s' did not send because it is an empty file" % file)
        pass
    else:
        if file in sentFiles: ## check file has been send already.
            print("'%s' has already been sent to server." % file)
            pass
        else: ## send file to server
            print("Sending File %s to Server:" % file)
            framedSend(s, str.encode(file),debug)
            sentFiles.append(file) ## add filename to sentFile list
            try: ## try to open file but handle if file does not exist
                with open(file, "r") as f: ## open file
                    for line in f:
                        framedSend(s, str.encode(line),debug)
                        print("Server Received: ",framedReceive(s,debug))
                    print("Server Coppied: '%s'\n" % file)
                f.close()
            except IOError:
                print("'%s' could not be open because it dosnt exist" % file)

f.close()
s.close() ## no more files to send close socket.
        
