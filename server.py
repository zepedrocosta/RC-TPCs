import sys
import socket
import pickle
import os

"""
@author: Catarina Gonçalves Costa | 62497
@author: José Pedro Pires Costa | 62637
"""

localIP = "127.0.0.1"
portSP = sys.argv[1]
bufferSize = 1024
status = -1

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, portSP))


def main():
    while True:
        global status
        message, address = UDPServerSocket.recvfrom(bufferSize)
        request = pickle.loads(message)
        fileName = request[0]
        offset = request[1]
        noBytes = request[2]
        if not os.path.isfile(fileName):
            status = 1
        elif (noBytes * offset) >= os.path.getsize(fileName):  # VERIFICAR
            status = 2
        else:
            status = 0
        file = open(fileName, "r")
        file.seek(offset)
        data = file.read(noBytes) # Informação lida
        # bytesRead = os.path.getsize(fileName) - noBytes * offset
        # reply = (0, data, )


main()
