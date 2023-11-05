import sys
import socket
import pickle
import select
import random

senderIP = int(sys.argv[1])
senderPort = int(sys.argv[2])
receiverIP = int(sys.argv[3])
receiverPort = int(sys.argv[4])
filename = sys.argv[5]
windowSizeInBlocks = int(sys.argv[6])

base = 1
nextSeqNum = 1
chunkSize = 1024
packets = []

class cStates:
    INITIAL_STATE
    
recieverAddressPort = (receiverIP, receiverPort)

UDPSenderSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# # Bind to address and ip
# UDPSenderSocket.bind((receiverIP, receiverPort))

def waitForReply( uSocket, timeOutInSeconds ): 
    rx, tx, er = select.select( [uSocket], [], [], timeOutInSeconds) 
    # waits for data or timeout 
    if rx == []: 
        return False 
    else: 
        return True 
    
def sendDatagram (msg, sock, address): 
    # msg is a byte array ready to be sent 
    # Generate random number in the range of 1 to 10 
    rand = random.randint(1, 10) 
    # If rand is less is than 3, do not respond (20% of loss probability) 
    if rand >= 3: 
        sock.sendto(msg, address) 

def recv_ack(data):        
       msgRecv = pickle.loads(data)
       base = msgRecv[1]
       if(base >= nextSeqNum): # o package foi recebido
           stop_timer
        else: # o package foi perdido a enviar/ voltar a enviar
            start_timer


def rdt_sent(data):
    if(nextSeqNum < base + windowSizeInBlocks):
        msgSendP = pickle.dumps((nextSeqNum,data))
        sendDatagram(msgSendP, UDPSenderSocket, recieverAddressPort)
        if(base==nextSeqNum):
            start_timer
        nextSeqNum+=1
       # recv_ack()


def main():
    global base
    global nextSeqNum
    file = open(filename, "rb")
    seqN = 0 # Tamanho em 'packets'
    while True:
        data = file.read(chunkSize)
        if not data:
            break  # End of file
        packet = pickle.dumps((seqN, data))
        packets.append(packet)
        seqN += 1

    state = cStates.INITIAL_STATE 
    while state != FINAL_STATE: 
        match state:
            case cStates.INITIAL_STATE:
                base = 1
                nextSeqNum = 1
                break
            case cStates.STATE_1: # enviar packets
                rdt_sent(data)
                state = STATE_2
                break
            case cStates.STATE_2: #receber ack
                recv_ack()
                break
            case cStates.STATE_3: #timeout
                break






main()