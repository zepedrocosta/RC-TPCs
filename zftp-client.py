# python zftp-client.py localhost 20001
# import os para ver se o file existe

import socket
import sys

openTCP = True

server_name = sys.argv[1]

localPort = int(sys.argv[2])
serverAddressPort = ("127.0.0.1", localPort)
bufferSize = 1024


# Open command
def openCon(args):
    x = len(args)
    global port
    port = int(args[1])
    if x != 2:
        print("Invalid number of arguments")
    elif port > 65535:
        print("Invalid port number")
    else:
        string = " ".join(args)
        input = str.encode(string)
        UDPClientSocket.sendto(input, serverAddressPort)
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode()
        print(msg)


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


def getFile(args):
    # SERVER -> CLIENT
    if(len(args) == 2):
        fileName = args[1]
    else:
        fileName = args[2]
    string = " ".join(args)
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


def putFile(args):
    # CLIENT -> SERVER
    fileName = args[1]
    string = " ".join(args)
    input = str.encode(string)
    UDPClientSocket.sendto(input, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = msgFromServer[0].decode()
    print(msg)
    if msg == "ack":
        TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPClientSocket.connect((str(server_name), int(port)))
        #TCPClientSocket.send(fileName.encode())
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
    global UDPClientSocket
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    while openTCP:
        cmd = input()
        args = cmd.split(" ")
        switch_case(args)


main()
