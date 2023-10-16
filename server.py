import sys
import socket
import pickle
import os
import random

"""
@author: Catarina Gonçalves Costa | 62497
@author: José Pedro Pires Costa | 62637
"""

localIP = "127.0.0.1"
portSP = sys.argv[1]
bufferSize = 1024
status = -1
# cOffset = 0

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, portSP))


def serverReply(msgP, UDPServerSocket, address):
    randomNumber = random.randint(0, 10)
    if randomNumber >= 3:
        UDPServerSocket.sendto(msgP, address)
    return


def main():
    while True:
        global status
        message, address = UDPServerSocket.recvfrom(bufferSize)
        request = pickle.loads(message)
        fileName = request[0]
        offset = request[1]
        chunkSize = request[2]
        if not os.path.isfile(fileName):  # Ficheiro não existe no server
            status = 1
        elif chunkSize > os.path.getsize(fileName):  # VERIFICAR
            status = 2
        else:
            status = 0
        file = open(fileName, "r")
        file.seek(offset)
        data = file.read(chunkSize)  # Informação lida
        bytesRead = os.path.getsize(fileName) - offset # VERIFICAR
        msg = (status, bytesRead, data)
        msgP = pickle.dumps(msg)
        serverReply(msgP, UDPServerSocket, address)


main()
