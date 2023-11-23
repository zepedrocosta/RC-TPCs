import sys
import socket
from threading import Thread
from queue import Queue
import requests

"""
@author: Catarina Gonçalves Costa | 62497
@author: José Pedro Pires Costa | 62637
"""

baseURL = sys.argv[1]
movieName = sys.argv[2]
track = sys.argv[3]

TCPPlayerSocket = socket.socket(
    family=socket.AF_INET, type=socket.SOCK_STREAM
)  # create TCP welcoming socket
TCPServerSocket = socket.socket(
    family=socket.AF_INET, type=socket.SOCK_STREAM
)  # create TCP welcoming socket

def producer(queue):
    path = baseURL + '/' + movieName
    print(path)
    # r = requests.get(path)

def consumer(queue):
    print('consumer')

def main():
    queue = Queue()
    
    # Consumer
    consumerThread = Thread(target=consumer, args=(queue))
    consumerThread.start()

    # Producer
    producerThread = Thread(target=producer, args=(queue))
    producerThread.start()

    # Finish
    producerThread.join()
    consumerThread.join()


main()
