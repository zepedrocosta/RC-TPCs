import socket
import subprocess
import os

"""
@author: Catarina Gonçalves Costa | 62497
@author: José Pedro Pires Costa | 62637
"""

# Start a socket listening for connections on 0.0.0.0:8000
# (0.0.0.0 means all interfaces)
server_socket = socket.socket()
server_socket.bind(("localhost", 8000))
server_socket.listen(0)
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile("rb")

# Player used
try:
    cmdline = "MPlayer-generic-r38407+g10a56363a7/mplayer.exe -ni -"  
    player = subprocess.Popen(cmdline.split(), stdin=subprocess.PIPE)
    while True:
        # Repeatedly read 1k of data from the connection and write it to
        # the media player's stdin
        data = connection.read(1024)
        if not data:
            break
        player.stdin.write(data)
finally:
    connection.close()
    server_socket.close()
    player.terminate()
