"""
Network scanner client module.
"""

import socket

HOST = "127.0.0.1"
PORT = 500008

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    sock.sendall(b'Hello, world')
    data = sock.recv(1024)

print('Received', repr(data))
