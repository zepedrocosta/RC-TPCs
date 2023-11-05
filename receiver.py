import sys
import socket
import pickle
import random
import select

receiverIP = int(sys.argv[1])
receiverPort = int(sys.argv[2])
fileNameInReceiver = sys.argv[3]
bufferSize = 1024
expectedSeqNum = 0

# Create a datagram socket
UDPReceiverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPReceiverSocket.bind((receiverIP, receiverPort))


def waitForReply(uSocket, timeOutInSeconds):
    rx, tx, er = select.select([uSocket], [], [], timeOutInSeconds)
    # waits for data or timeout
    if rx == []:
        return False
    else:
        return True


def sendDatagram(msg, sock, address):
    # msg is a byte array ready to be sent
    # Generate random number in the range of 1 to 10
    rand = random.randint(1, 10)
    # If rand is less is than 3, do not respond (20% of loss probability)
    if rand >= 3:
        sock.sendto(msg, address)


def main():
    global expectedSeqNum
    file = open(fileNameInReceiver, "wb")  # Cria ficheiro novo
    while True:
        if waitForReply(
            UDPReceiverSocket, 1
        ):  # Espera um segundo pela informação a ser lida 'AJUSTAR'
            datagram, address = UDPReceiverSocket.recvfrom(bufferSize)
            message = pickle.loads(datagram)
            seqN = message[0]
            data = message[1]
            print("Received packet: ", seqN)
            if seqN == expectedSeqNum:
                file.write(data)
                expectedSeqNum += 1
                reply = (expectedSeqNum, "ACK")
                replyP = pickle.dumps(reply)
                sendDatagram(replyP, UDPReceiverSocket, address)
                print("Sending ACK", expectedSeqNum)
            else:
                reply = (
                    expectedSeqNum - 1,
                    "ACK",
                )  # Caso em que recebe um packet diferente daquele que está á espera
                replyP = pickle.dumps(reply)
                sendDatagram(replyP, UDPReceiverSocket, address)
                print("Sending ACK", expectedSeqNum - 1)
        else:
            break


main()
