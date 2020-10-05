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
outfile = input("What file would you like to send ? ")# ask for file name

if exists(outfile):
    file = open(outfile,'rb')## if file exist open file
    file_data = file.read()## read file
    if len(file_data) == 0:## check for emtpy file
        print("cant send empty file")
        sys.exit(0)
    else: ## file is not empty
        framedSend(s,outfile.encode(),debug) ## send file name to check if exists in server
        server_check = framedReceive(s,debug) ## wait for responce from server if file exists
        server_check = server_check.decode()
        if server_check == 'True':
            print("File in server already")
            sys.exit(0)
        else:
            try: ##send non-duplicate file payload to server
                framedSend(s, file_data, debug) ## ADDED ENCODE
            except:
                print("Connection to server lost...")
                sys.exit(0)
            try: ##wait for done responce from server.
                serverMsg = framedReceive(s,debug)
                print("Server says: %s" % serverMsg.decode())
            except:
                print("Connection to server lost...")
            
                
#if exists(outfile):
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
#                print("Connection to server lost...")
#                sys.exit(0)
#            try:
#                framedReceive(s,debug)
#            except:
#                print("Connection to server lost...")
#else:
#    print("File Does not exist try again later...")
#    sys.exit(0)##






#def len_check(file):
#    return len(file.encode('utf-8'))#
#
#if exists(outfile):
#    file = open(outfile, 'r')
#    payload = file.read()
#    if len(payload) == 0:
#        print("Empty File did not send")
#        sys.exit(0)
#    else:
#        framedSend(s, outfile.encode(), debug)
#        framedSend(s, payload.encode(), debug)
#        print("recived: ", framedReceive(s, debug))
#        sys.exit(0)
#else:
#    print("file dosnt exit")
#    sys.exit(0)




#try:
#    if is_empty_file(outfile) == False:
#        print("Could not send because file is empty")
#        sys.exit(0)
#    framedSend(s, str.encode(outfile), debug) ## Send filename
#    print("Sending: '%s'..." % outfile)#
#    file = open(outfile, 'r') ## open file if not empty
#    payload = file.read() ## read contents of file
#except IOError:
#    print("File does not exist")
#if exists(outfile):
#    file = open(outfile,'r')## if file exist open file
#    file_data = file.read()## read contents of file
#    if len(file_data) == 0:
#        print("Did not send since Empty file.")
#        sys.exit(0)
#    else:
#        print("Sending %s to Server" % outfile)
#        framedSend(s, str.encode(outfile), debug)## send filename to server to check if it exist
#        in_server = framedReceive(s, debug) ## Receive boolean if file exist in server
#        in_server = in_server.decode()
#        if in_server == "True":
#           print("Already exist on server.")
#           sys.exit(0)
#        else:
#            framedSend(s, str.encode(file_data), debug)##if file isnt already on server send data
     #       #server_read = framedReceive(s, debug)## receive what data was copied into server
     #       #server_read = server_read.decode()
#            print("Server has received %s and wrote its contents to file." % outfile)
#            s.close()

#else:
#    print("Sorry cant find %s or doesnt exist" % outfile)
#    sys.exit(0)
    
    
#sentFiles = []
#files = ["testfile.txt", "file1.txt", "emptyfile.txt", "file3.txt", "file1.txt", "nonexistentFile.txt","code.py"]


#def is_empty_file(filename):
#    return os.path.isfile(filename) and os.path.getsize(filename) 
#
#for file in files:
#    if is_empty_file(file) == False:
#        print("'%s' did not send because it is an empty file\n" % file)
#        pass
#    else:
#        if file in sentFiles: ## check file has been send already.
#            print("'%s' tried to send but already has been sent to server." % file)
#            pass
#        else: ## send file to server
#            print("Sending File %s to Server:" % file)
#            sentFiles.append(file)## add filename to sent list
#            framedSend(s, str.encode(file),debug)##Send Filename to server
#            #sentFiles.append(file) ## add filename to sentFile list
#            try: ## try to open file but handle if file does not exist
#                quitMsg = "exit"
#                with open(file) as f: ## open file
#                    for line in f:
#                        framedSend(s, str.encode(line),debug)
#                        print("Server Received: ",framedReceive(s,debug))
#                    print("Server Coppied: '%s'\n" % file)
#                framedSend(s,str.encode(quitMsg),debug)
#                f.close()
#            except IOError:
#                print("'%s' could not be open because it dosnt exist" % file)
#
#f.close()
#s.close() ## no more files to send close socket.
        
