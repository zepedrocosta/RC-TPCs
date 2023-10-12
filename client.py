import sys
import socket
import pickle

"""
@author: Catarina Gonçalves Costa | 62497
@author: José Pedro Pires Costa | 62637
"""

host_of_server = sys.argv[1]
portSP = int(sys.argv[2])
fileName = sys.argv[3]
chunkSize = sys.argv[4]

serverAddressPort = ("127.0.0.1", portSP)

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


def main():
    file = open(fileName, "wb")
    offset = 0
    while True:
        request = (fileName, offset)  # Falta blockSize
        req = pickle.dumps(request)
        UDPClientSocket.sendto(req, serverAddressPort)


main()
