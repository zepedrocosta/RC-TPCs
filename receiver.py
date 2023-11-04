import sys
import socket
import pickle
import random
import select

receiverIP = int(sys.argv[1])
receiverPort = int(sys.argv[2])
fileNameInReceiver = sys.argv[3]
bufferSize = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# # Bind to address and ip
# UDPServerSocket.bind((receiverIP, receiverPort))

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


def main()
    while True:
        message, address = UDPServerSocket.recvfrom(bufferSize)
        msgRecv = pickle.loads(message)
        nSeq = msgRecv[1]
        data = msgRecv[2]

        print("recieved nSeq:"+nSeq)

        
    

main()