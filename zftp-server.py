# python zftp-server.py 20001

import os
import socket

import sys

localIP = "127.0.0.1"
localPort = int(sys.argv[1])
bufferSize = 1024

ackBytes = str.encode("ack")
nack1Bytes = str.encode("nack 1")
nack2Bytes = str.encode("nack 2")
nack3Bytes = str.encode("nack 3")
openPort = False


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))


def openCon(args):
    x = len(args)
    global port
    global openPort
    port = int(args[1])
    if x != 2:
        UDPServerSocket.sendto(nack1Bytes, address)
    elif port > 65535:
        UDPServerSocket.sendto(nack2Bytes, address)
    elif openPort == False:
        openPort = True
        UDPServerSocket.sendto(ackBytes, address)
        print("Port received")
    else:
        print("Server already has a port")


def closeCon():
    global openPort
    if openPort == True:
        openPort = False
        UDPServerSocket.sendto(ackBytes, address)
        UDPServerSocket.close
        print("Interaction closed")
    else:
        UDPServerSocket.sendto(nack1Bytes, address)
        print("No interaction")


def getFile(args):
    if len(args) > 4 or len(args) == 1:
        UDPServerSocket.sendto(nack1Bytes, address)
        print("Invalid number of arguments")
    elif args[3] == "True":
        UDPServerSocket.sendto(nack2Bytes, address)
        print("File already exists on client")
    elif not os.path.isfile(args[1]):
        UDPServerSocket.sendto(nack3Bytes, address)
        print("File does not exist")
    else:
        UDPServerSocket.sendto(ackBytes, address)
        TCPserverSocket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM
        )  # create TCP welcoming socket
        TCPserverSocket.bind(("", int(port)))
        TCPserverSocket.listen(1)
        TCPclientSocket, addr = TCPserverSocket.accept()
        with open(args[1], "rb") as file:
            while True:
                data = file.read(bufferSize)
                if not data:
                    break
                TCPclientSocket.send(data)
        TCPclientSocket.close()
        TCPserverSocket.close()
        print("File sent")


def putFile(args):
    if len(args) > 4 or len(args) == 1:
        UDPServerSocket.sendto(nack1Bytes, address)
        print("Invalid number of arguments")
    elif args[3] == "False":
        UDPServerSocket.sendto(nack2Bytes, address)
        print("File does not exist on client")
    elif os.path.isfile(args[2]):
        UDPServerSocket.sendto(nack3Bytes, address)
        print("File already exists on server")
    else:
        UDPServerSocket.sendto(ackBytes, address)
        TCPserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPserverSocket.bind(("", int(port)))
        TCPserverSocket.listen(1)
        TCPclientSocket, addr = TCPserverSocket.accept()
        if len(args) == 2:
            fileName = args[1]
        else:
            fileName = args[2]
        with open(fileName, "wb") as file:
            while True:
                data = TCPclientSocket.recv(bufferSize)
                if not data:
                    break
                file.write(data)
        TCPclientSocket.close()
        TCPserverSocket.close()
        print("File sent")


def main():
    print("ZFTP-Server up and listening")

    while True:
        messageReceived = UDPServerSocket.recvfrom(bufferSize)

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
