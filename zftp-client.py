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
    # Fechar
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
    fileName = args[1]
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
        TCPclientSocket.connect(
            (str(server_name), int(port))
        )  # open TCP connection ERRORRRR
        with open(fileName, "wb") as file:
            while True:
                data = TCPclientSocket.recv(bufferSize)
                if not data:
                    break
                file.write(data)
        TCPclientSocket.close()


def putFile(args):
    print


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
    # Create a UDP socket at client side

    global UDPClientSocket
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    while openTCP:
        cmd = input()
        args = cmd.split(" ")
        switch_case(args)


main()
