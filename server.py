"""
Network scanner server module.
"""

import ipaddress
import socket
import threading
import logging

HOST = ""
PORT = 50009


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", 
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)

def start_sever() -> None:
    """Start server and wait for incoming connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(1)

        while True:
            try:
                client_sock, addr = sock.accept()
                client_thread = threading.Thread(
                    target=handle_client_connection,
                    args=(client_sock, addr),
                )
                client_thread.start()
            except Exception as e:
                print(e)


def handle_client_connection(client_socket: socket.socket, client_address: tuple) -> None:
    """Handle client connection in a new thread."""
    with client_socket:
        logger.debug(f"Connected by: {client_address}")
        data = client_socket.recv(1024).decode()

        subnet = ipaddress.ip_network(data)

        for ip in subnet.hosts():
            scan_ip(ip, 80)

        client_socket.sendall(data.encode())
    


def scan_ip(host: str, port: int) -> None:
    """Check if a host is up by connecting to port 80."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((str(host), port))
        except Exception as e:
            print("ERROR:", e, host, port)


if __name__ == "__main__":
    start_sever()