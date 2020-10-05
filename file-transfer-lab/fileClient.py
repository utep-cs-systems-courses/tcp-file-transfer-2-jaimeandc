#! /usr/bin/env python3

import socket, sys, re
import os.path
from os import path
from os.path import exists
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

file_name = input("Choose a file")
if exists(file_name):
    file = open(file_name, 'rb')
    payload = file.read()
    if len(payload) == 0:
        print("Cant Send empty file")
        sys.exit(0)
    else:
        new_file_name = input("give that file a new name in server")
        framedSend(s, new_file_name.encode(), debug)
        file_exists = framedReceive(s,debug)
        file_exists = file_exists.decode()
        if file_exists == 'True':
            print("That filename exist allready")
            sys.exit(0)
        else:
            try:
                framedSend(s, payload,debug)
            except:
                print("Lost connection with server while sending file contents")
                sys.exit(0)
            try:
                framedReceive(s,debug)
            except:
                print("Lost connection with server while receiving data")
                sys.exit(0)
else:
    print("File Doesnt Exist")
    sys.exit(0)
                
    


#outfile = input("What file would you like to send ? ")# ask for file name
#outfile = outfile.encode('utf-8')
#if exists(outfile):
#    file = open(outfile,'rb')## if file exist open file
#    file_data = file.read()## read file
#    if len(file_data) == 0:## check for emtpy file
#        print("cant send empty file")
#        sys.exit(0)
#    else: ## file is not empty
#        framedSend(s,outfile,debug) ## send file name to check if exists in server
#        server_check = framedReceive(s,debug) ## wait for responce from server if file exists
#        server_check = server_check.decode()
#        if server_check == 'True':
#            print("File in server already")
#            sys.exit(0)
#        else:
#            try: ##send non-duplicate file payload to server
#                print("will send at this point")
#                #framedSend(s, file_data, debug) ## ADDED ENCODE
#            except:
#                print("Connection to server lost...")
#                sys.exit(0)
#            try: ##wait for done responce from server.
#                serverMsg = framedReceive(s,debug)
#                print("Server says: %s" % serverMsg.decode())
#            except:
#                print("Connection to server lost...")
            
                
#if exidsts(outfile):
#    file = open(outfile, 'rb')
#    file_payload = file.read()
#    if len(file_payload) == 0:
#        print("Empty file try again later")
#        sys.exit(0)
#    else:
#        framedSend(s, outfile.encode(), debug)
#        server_check = framedReceive(s, debug)
#        server_check = server_check.decode()
#        if server_check == 'True':
#            print("Sorry file exist in server already try again later...")
#            sys.exit(0)
#        else:
#            try:
#                framedSend(s, file_payload, debug)
#            except:
#                print("Connection to server lost sending file payload")
#                sys.exit(0)
#            try:
#                framedReceive(s,debug)
##            except:
#                print("Connection to server lost while receiving data")
#else:
#    print("File Does not exist try again later...")
#    sys.exit(0#)
