#! /usr/bin/env python3
import sys
sys.path.append("../lib") # For params
import re, socket, params, os
from os.path import exists

from framedSock import framedSend, framedReceive
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
#received_files = []

while True:
    sock, addr = listsock.accept()
    print("Connected to client", addr)
    if not os.fork():
        while True:
            payload = framedReceive(sock,debug)
            if not payload:
                break
            payload = payload.decode()

            if exists(payload):
                framedSend(sock, b"True", debug)
            else:
                framedSend(sock, b"False", debug)
                
                try:
                    payload2 = framedReceive(sock, debug)
                except:
                    print("Connection with client lost will receiving file data")
                    sys.exit(0)
                    
                if not payload2:
                    break
                payload2 += b"!"
                try:
                    framedSend(sock, payload2, debug)
                except:
                    print("Connection lost with client while sending data.")
                    
                output = open(payload, 'wb')
                output.write(payload2)
                sock.close()








####### WHAT I DID 
#while True:
#    conn, addr = listsock.accept()
#    print("Incoming connection from ", addr)
#    if not os.fork():
#        while True:
#            filename = framedReceive(conn,debug)
#            #newfile = filename.decode('utf-8')
#            print(filename)
#            if filename in received_files:
#                print("EXIST")
#                framedSend(conn,b"True",debug) ## send message to client that file is duplicate
#            else:## if new file
#               # received_files.append(newfile)
#                framedSend(conn,b"False", debug)
#                try:
#                    #received_files.append(newfile)
#                    #payload = framedReceive(conn,debug) ## receive file contents
#                    #if not payload:
#                    #    print("Done")
#                    #    break
#                    #with open("test.txt", "wb") as file2:
#                    #    file2.write(payload)
#                    print("will receive payload and wirte")
#                except:
#                    print("Connection to Client was lost 1")
#                    framedSend(conn,str.encode("Problem occured 1"), debug)
#                    break
#                try:
#                    framedSend(conn,str.encode("Server wrote file"),debug)
#                except:
#                    print("Connection to client was lost...")
#                    framedSend(conn,str.encode("Couldnt write to file"),debug)
#                    break
