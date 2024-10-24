"""
Network scanner server module.
"""

import socket

HOST = ""
PORT = "50008"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(1)
    client_sock, addr = sock.accept()

    with client_sock:
        print("Connected by", addr)
        while True:
            data = client_sock.recv(1024)
            if not data: break
            client_sock.sendall(data)
            