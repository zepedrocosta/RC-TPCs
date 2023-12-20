import sys
import socket
import pickle
import select
import time

"""
@author: Catarina Gonçalves Costa | 62497
@author: José Pedro Pires Costa | 62637
"""

host_of_server = sys.argv[1]
portSP = int(sys.argv[2])
fileName = sys.argv[3]
chunkSize = int(sys.argv[4])

buffer = chunkSize + 4096

serverAddressPort = ("127.0.0.1", portSP)

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


def waitForReply(UDPClientSocket):
    rx, tx, er = select.select([UDPClientSocket], [], [], 1)
    if rx == []:
        return False
    else:
        return True


def main():
    start = time.time()
    file = open(
        fileName, "wb"
    )  # Cria um ficheiro com o mesmo nome do ficheiro do server
    offset = 0
    while True:
        request = (fileName, offset, chunkSize)
        req = pickle.dumps(request)
        UDPClientSocket.sendto(req, serverAddressPort)
        if waitForReply(UDPClientSocket):
            datagram, address = UDPClientSocket.recvfrom(buffer)
            message = pickle.loads(datagram)
            status = message[0] 
            if status == 0:
                len_data = message[1]
                data = message[2]
                file.write(data)
                offset += chunkSize
                if len_data < chunkSize:
                    break
            else:
                break
    print(f"status = {status}")
    UDPClientSocket.close()
    file.close()
    end = time.time()
    elapsedTime = end - start
    transferSpeed = (offset / elapsedTime) /1024
    print(f"Transfer speed = {transferSpeed} Kb/s")


main()
