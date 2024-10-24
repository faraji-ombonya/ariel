"""
Network scanner client module.
"""

import socket

HOST = "127.0.0.1"
PORT = 50009

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    sock.sendall(b'192.168.1.0/24')
    data = sock.recv(1024)

print('Received', repr(data))
