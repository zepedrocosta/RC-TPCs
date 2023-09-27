# python zftp-server.py 20001

import socket
import sys

localIP = "127.0.0.1"
localPort = int(sys.argv[1])
bufferSize = 1024

msgFromServer = "ack"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("ZFTP-Server up and listening")

while True:
    messageReceived = UDPServerSocket.recvfrom(bufferSize)

    clientMsg = messageReceived[0]
    address = messageReceived[1]

    TCPport = clientMsg.decode()

    # Sending open reply to client

    UDPServerSocket.sendto(bytesToSend, address)
