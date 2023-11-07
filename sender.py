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
windowSizeInBlocks = 5

base = 1
nextSeqNum = 1
chunkSize = 1024
packets = []
window = {}
currWindow = 0
seqN = 0

class cStates:
    INITIAL_STATE = "inicio"
    FINAL_STATE = "final"
    STATE_1 = "state_1"

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
    if rand >= 3:
        sock.sendto(msg, address)


def recv_ack(data):
    global nextSeqNum
    msgRecv = pickle.loads(data)
    # base = msgRecv[1]
    base = msgRecv[0]
    if base == nextSeqNum - 1:  # o package foi recebido com sucesso no receiver
        print("Recebeu ack certo")
        return True
    else:  # o package foi perdido a enviar/ voltar a enviar
        print("Recebeu ack errado")
        return False


def rdt_sent():
    # enviar window nextSeqNum ate windowSizeInBlocks 1 a 1
    # esperar timeout
    global currWindow
    global nextSeqNum
    global base
    while currWindow < len(window):
        # print(str(currWindow))
        tmp = window[str(currWindow)]
        i = 0
        while i < len(tmp): # corrigir a len
            msgSendP = pickle.dumps(
                (nextSeqNum, tmp[i])
            )  # manda um a um dentro da window
            print("Packet sent: ", nextSeqNum)
            i += 1
            sendDatagram(msgSendP, UDPSenderSocket, recieverAddressPort)
            recieved = False
            nextSeqNum += 1
            if waitForReply(UDPSenderSocket, 2):  # espera 5 segundos por info
                datagram, address = UDPSenderSocket.recvfrom(chunkSize)
                recieved = recv_ack(datagram)
            else:
                print("Perdeu-se ACK: ", nextSeqNum - 1)
                nextSeqNum-=i
                break
        if recieved: # se tudo correu bem
            currWindow += 1
        elif base == len(window[str(len(window) - 1)]) and recieved: #para parar
            # sendDatagram("", UDPSenderSocket, recieverAddressPort)
            global status
            status = cStates.FINAL_STATE
            return
        # else: #testar
        #     nextSeqNum = currWindow * chunkSize
        rdt_sent()


def prepareWindow():
    global packets
    global windowSizeInBlocks
    global window
    global chunkSize
    global seqN
    file = open(filename, "rb")
    i = 1
    while True:
        data = file.read(chunkSize)
        packets.append(data)  # separar o ficheiro em packets
        seqN += 1
        if not data: # fim do ficheiro
            i = windowSizeInBlocks
        if i == windowSizeInBlocks:
            index = len(window)
            window[str(index)] = packets
            packets = []
            i = 1
            if len(data) < chunkSize:
                break
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
            case cStates.STATE_1:  # enviar packets
                rdt_sent()
    UDPSenderSocket.close()


main()
