# python zftp-client.py server_name 20001

import socket
import sys

openTCP = True

server_name = sys.argv[1]

localPort = int(sys.argv[2])
serverAddressPort = ("127.0.0.1", localPort)
bufferSize = 1024


def openCon(args):
    x = len(args)
    if x != 2:
        print("Invalid number of arguments")
    port = args[1]
    if port > 65535:
        print("Invalid port number")
    # Enviar via UDP a porta
    
def closeCon(args):
    # Fechar TCP
    global openTCP
    openTCP = False


def getFile(args):
    print


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
        print("Invalid case selected.")


def main():
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while openTCP:
        cmd = input()
        args = cmd.split(" ")
        switch_case(args)


main()
