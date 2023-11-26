import sys
import socket
from threading import Thread
from queue import Queue
import requests
import linecache

"""
@author: Catarina Gonçalves Costa | 62497
@author: José Pedro Pires Costa | 62637
"""

baseURL = sys.argv[1]
movieName = sys.argv[2]
track = int(sys.argv[3])

playerAddressPort = ("localhost", 8000)

TCPPlayerSocket = socket.socket(
    family=socket.AF_INET, type=socket.SOCK_STREAM
)  # create TCP welcoming socket


def producerTask(queue):
    numberOfSegments = linecache.getline(
        "manifest.txt", 7
    ).strip()  # Numero de segmentos
    segmentNameLine = (
        2 + track + ((int(numberOfSegments) + 4) * (track - 1))
    )  # Line for the track name
    segmentLinesBegin = 2 + (5 * track) + (int(numberOfSegments) * (track - 1))
    path = baseURL + movieName
    r = requests.get(path + "/manifest.txt")
    with open("manifest.txt", "wb") as f:
        f.write(r.content)
    segmentName = linecache.getline("manifest.txt", segmentNameLine).strip()
    for i in range(1, int(numberOfSegments) + 1):
        segment = linecache.getline(
            "manifest.txt", int(segmentLinesBegin) + i
        ).strip()
        list = segment.split()
        beginAndEnd = [int(num) for num in list]
        begin = beginAndEnd[0]
        end = beginAndEnd[1]
        headers = {"Range": "bytes={}-{}".format(begin, end)}
        r = requests.get(path + "/" + segmentName, headers=headers)
        queue.put(r.content)
        print("Segmento {} enviado!".format(i))
    queue.put(None)  # Fim do segmento
    print("Producer done!!")

def consumerTask(queue):
    TCPPlayerSocket.connect(playerAddressPort)
    count = 1
    while True:
        item = queue.get()
        if item is None:
            break
        TCPPlayerSocket.send(item)
        print("Segmento {} recebido!".format(count))
        count += 1
    print("Consumer done!!")
    TCPPlayerSocket.close()


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
