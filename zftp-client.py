# python zftp-client.py server_name 20001

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
        port = str.encode(args[1])
        UDPClientSocket.sendto(port, serverAddressPort)
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode()
        print(msg)


def closeCon():
    # Fechar
    UDPClientSocket.close()
    global openTCP
    openTCP = False


def getFile(args):
    # criar socket TCP
    print


def putFile(args):
    print


def switch_case(args):
    if args[0] == "open":
        openCon(args)
    elif args[0] == "close":
        closeCon()
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
