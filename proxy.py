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

TCPPlayerSocket = socket.socket(
    family=socket.AF_INET, type=socket.SOCK_STREAM
)  # create TCP welcoming socket


def producerTask(queue):
    segmentNameLine = 2 + track + (54 * (track - 1))  # Line for the track name
    segmentBegin = 2 + (5 * track) + (50 * (track - 1))  # 50
    path = baseURL + movieName
    r = requests.get(path + "/manifest.txt")
    with open("manifest.txt", "wb") as f:
        f.write(r.content)
    segmentName = linecache.getline("manifest.txt", segmentNameLine).strip()
    for i in range(1, 51):
        numberOfSegments = linecache.getline(
            "manifest.txt", segmentBegin + i
        ).strip()
        list = numberOfSegments.split()
        beginAndEnd = [int(num) for num in list]
        begin = beginAndEnd[0]
        end = beginAndEnd[1]
        headers = {"Range": "bytes={}-{}".format(begin, end)}
        r = requests.get(path + "/" + segmentName, headers=headers)
        queue.put(r.content)
        print("Segmento {} enviado!".format(i))
    queue.put(None) # Fim do segmento

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
