# python zftp-server.py 20001

import os.path
import socket

import sys

localIP = "127.0.0.1"
localPort = int(sys.argv[1])
bufferSize = 1024

ackBytes = str.encode("ack")
nackBytes = str.encode("nack")
openPort = False


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))


def openCon(args):
    global openPort
    if openPort == False:
        openPort = True
        global port
        port = args[1]
        UDPServerSocket.sendto(ackBytes, address)
    else:
        UDPServerSocket.sendto(nackBytes, address)


def closeCon():
    global openPort
    if openPort == True:
        openPort = False
        UDPServerSocket.sendto(ackBytes, address)
        UDPServerSocket.close
    else:
        UDPServerSocket.sendto(nackBytes, address)


def getFile(args):
    if os.path.isfile(args[1]):
        UDPServerSocket.sendto(ackBytes, address)
    else:
        UDPServerSocket.sendto(nackBytes, address)
    
    TCPserverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # create TCP welcoming socket
    TCPserverSocket.bind(("", int(port)))
    TCPserverSocket.listen(1)


def putFile(args):
    print


def main():
    print("ZFTP-Server up and listening")

    while True:
        messageReceived = UDPServerSocket.recvfrom(bufferSize)

        # Sending open reply to client

        clientMsg = messageReceived[0]
        global address
        address = messageReceived[1]

        message = clientMsg.decode()
        args = message.split(" ")
        if args[0] == "open":
            openCon(args)
        elif args[0] == "close":
            closeCon()
        elif args[0] == "get":
            getFile(args)
        elif args[0] == "put":
            putFile(args)


main()
