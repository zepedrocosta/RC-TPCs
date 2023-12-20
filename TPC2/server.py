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
portSP = int(sys.argv[1])
bufferSize = 1024
status = -1
data = ""

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, portSP))


def serverReply(msgP, UDPServerSocket, address):
    randomNumber = random.randint(1, 10)
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
        noBytes = request[2]
        print(f"file= {fileName},offset={offset}, noBytes={noBytes}")
        global data
        if not os.path.isfile(fileName):  # Ficheiro não existe no server
            status = 1
            print("Ficheiro não existe")
        elif offset > os.path.getsize(fileName) or offset < 0:
            status = 2
            print("Offset invalido")
        else:
            status = 0
            file = open(fileName, "rb")
            file.seek(offset)
            data = file.read(noBytes)  # Informação lida
        msg = (status, len(data), data)
        msgP = pickle.dumps(msg)
        serverReply(msgP, UDPServerSocket, address)


main()
