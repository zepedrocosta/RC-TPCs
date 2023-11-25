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


def producerTask(queue):
    path = baseURL + "/" + movieName
    print(path)
    # r = requests.get(path)


def consumerTask(queue):
    print("consumer")


def main():
    queue = Queue()

    # Consumer
    consumer = Thread(target=consumerTask, args=(queue,))
    consumer.start()

    # Producer
    producer = Thread(target=producerTask, args=(queue,))
    producer.start()

    # Finish
    producer.join()
    consumer.join()


main()
