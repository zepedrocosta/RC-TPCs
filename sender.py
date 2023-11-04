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

recieverAddressPort = (receiverIP, receiverPort)

UDPSenderSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

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

    
def main():
    file = open(filename, "rb")
    msgSend = (0, nSeq, data)
    msgSendP = pickle.dumps(msgSend)
    sendDatagram(msgSendP, UDPSenderSocket, recieverAddressPort)

    if waitForReply(UDPSenderSocket):



main()