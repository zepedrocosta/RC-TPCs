# python zftp-client.py localhost 20001

import socket
import sys
import os

"""
@author: Catarina Gonçalves Costa | 62497
@author: José Pedro Pires Costa | 62637
"""

openTCP = True

server_name = sys.argv[1]

localPort = int(sys.argv[2])
serverAddressPort = ("127.0.0.1", localPort)
bufferSize = 1024

# Create a datagram socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Open command
def openCon(args):
    global port
    string = " ".join(args)
    input = str.encode(string)
    UDPClientSocket.sendto(input, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = msgFromServer[0].decode()
    print(msg)
    if msg == "ack":
        port = int(args[1])


# Close command
def closeCon(args):
    string = " ".join(args)
    input = str.encode(string)
    UDPClientSocket.sendto(input, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = msgFromServer[0].decode()
    print(msg)
    UDPClientSocket.close()
    global openTCP
    openTCP = False


# get <File in server> <New file in client>
def getFile(args):
    # SERVER -> CLIENT
    if len(args) == 3:
        fileName = args[2]
    else:
        fileName = ""
    string = " ".join(args)
    # checks if the client already has a file with that name
    if os.path.isfile(fileName):
        string += " True"
    else:
        string += " False"
    input = str.encode(string)
    UDPClientSocket.sendto(input, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = msgFromServer[0].decode()
    print(msg)
    if msg == "ack":
        TCPclientSocket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM
        )  # create TCP welcoming socket
        TCPclientSocket.connect((str(server_name), int(port)))  # open TCP connection
        with open(fileName, "wb") as file:
            while True:
                data = TCPclientSocket.recv(bufferSize)
                if not data:
                    break
                file.write(data)
        TCPclientSocket.close()


# put <File in client> <New file in server>
def putFile(args):
    # CLIENT -> SERVER
    if len(args) == 3:
        fileName = args[1]
    else:
        fileName = ""
    string = " ".join(args)
    # checks if the client already has a file with that name
    if os.path.isfile(fileName):
        string += " True"
    else:
        string += " False"
    input = str.encode(string)
    UDPClientSocket.sendto(input, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = msgFromServer[0].decode()
    print(msg)
    if msg == "ack":
        TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPClientSocket.connect((str(server_name), int(port)))
        with open(fileName, "rb") as file:
            data = file.read(bufferSize)
            while data:
                TCPClientSocket.send(data)
                data = file.read(bufferSize)


def switch_case(args):
    if args[0] == "open":
        openCon(args)
    elif args[0] == "close":
        closeCon(args)
    elif args[0] == "get":
        getFile(args)
    elif args[0] == "put":
        putFile(args)
    else:
        print("Invalid command")


def main():
    while openTCP:
        cmd = input()
        args = cmd.split(" ")
        switch_case(args)


main()
