import sys
import socket
import pickle
import select
import random

# senderIP = sys.argv[1]
# senderPort = int(sys.argv[2])
# receiverIP = sys.argv[3]
# receiverPort = int(sys.argv[4])
# filename = sys.argv[5]
# windowSizeInBlocks = int(sys.argv[6])

senderIP = "127.0.0.1"
senderPort = 55555
receiverIP = "127.0.0.1"
receiverPort = 55555
filename = "test.txt"
windowSizeInBlocks = 1

base = 1
nextSeqNum = 1
chunkSize = 1024
packets = []
window = {}
currWindow = 0


class cStates:
    INITIAL_STATE = "inicio"
    FINAL_STATE = "final"
    STATE_1 = "state_1"
    STATE_2 = "state_2"
    STATE_3 = "state_3"


recieverAddressPort = (receiverIP, receiverPort)

UDPSenderSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# # Bind to address and ip
# UDPSenderSocket.bind((receiverIP, receiverPort))


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
    if rand >= 1:
        sock.sendto(msg, address)


def recv_ack(data):
    msgRecv = pickle.loads(data)
    # base = msgRecv[1]
    base = msgRecv[0]
    if base >= nextSeqNum:  # o package foi recebido com sucesso no receiver
        return True
    else:  # o package foi perdido a enviar/ voltar a enviar
        return False


def rdt_sent():
    #    if(nextSeqNum < base + windowSizeInBlocks):
    #        msgSendP = pickle.dumps((nextSeqNum,data))
    #        sendDatagram(msgSendP, UDPSenderSocket, recieverAddressPort)
    #        if(base==nextSeqNum):
    #            start_timer
    #        nextSeqNum+=1
    # recv_ack()

    # enviar window nextSeqNum ate windowSizeInBlocks 1 a 1
    # esperar timeout
    global currWindow
    global nextSeqNum
    if currWindow < len(window):
        print(str(currWindow))
        tmp = window[str(currWindow)]
        i = 0
        while i < len(tmp):
            msgSendP = pickle.dumps((nextSeqNum, tmp[i]))
            print(nextSeqNum)
            i += 1
            sendDatagram(msgSendP, UDPSenderSocket, recieverAddressPort)
            nextSeqNum += 1
        recieved = False
        while waitForReply(UDPSenderSocket, 5) is None:
            recieved = recv_ack()

        if recieved:
            currWindow += 1
        elif base == len(window[str(len(window) - 1)]) and recieved:
            global status
            status = cStates.FINAL_STATE
            return
        rdt_sent()


def prepareWindow():
    # MSG = pickle.dumps("start")
    # sendDatagram(MSG, UDPSenderSocket, recieverAddressPort)
    global packets
    file = open(filename, "rb")
    seqN = 0  # Tamanho em 'packets'
    i = 0
    while True:
        data = file.read(chunkSize)
        packet = pickle.dumps((seqN, data))
        packets.append(packet) # separar o ficheiro em packets
        seqN += 1 
        if not data:
            i = windowSizeInBlocks
            break  # End of file
        if i == windowSizeInBlocks:
            index = len(window)
            window[str(index)] = packets
            packets = []
            i = 0
        else:
            i += 1
    file.close()


def main():
    global base
    global nextSeqNum
    prepareWindow()

    state = cStates.INITIAL_STATE
    while state != cStates.FINAL_STATE:
        match state:
            case cStates.INITIAL_STATE:
                base = 1
                nextSeqNum = 1
                state = cStates.STATE_1
                # rdt_sent()
            case cStates.STATE_1:  # enviar packets
                rdt_sent()
                state = cStates.STATE_2
            case cStates.STATE_2:  # receber ack
                recv_ack()
            case cStates.STATE_3:  # timeout
                break
    UDPSenderSocket.close()


main()
