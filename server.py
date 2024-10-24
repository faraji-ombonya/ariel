"""
Network scanner server module.
"""

import ipaddress
import socket

HOST = ""
PORT = 50009


def start_sever():
    """Start server and wait for incoming connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(1)

        while True:
            try:
                client_sock, addr = sock.accept()
                with client_sock:
                    print("Connected by", addr)
                    data = client_sock.recv(1024).decode()

                    subnet = ipaddress.ip_network(data)

                    for ip in subnet.hosts():
                        scan_ip(ip, 80)

                    if not data: break  
                    client_sock.sendall(data.encode())
            except Exception as e:
                print(e)



def scan_ip(host: str, port: int) -> None:
    """Check if a host is up by connecting to port 80."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((str(host), port))
        except Exception as e:
            print("ERROR:", e, host, port)


if __name__ == "__main__":
    start_sever()