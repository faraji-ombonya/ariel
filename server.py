"""
Network scanner server module implemented with basic sockets.
"""

import ipaddress
import socket
import threading
import concurrent.futures
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


def handle_client_connection(
    client_socket: socket.socket, client_address: tuple
) -> None:
    """Handle client connection in a new thread.
    
    Use ThreadPoolExecutor to scan IPs concurrently.

    Arguments:
        client_socket (socket.socket): The client socket.
        client_address (tuple): The client address.

    Returns:
        None
    """
    with client_socket:
        logger.debug(f"Connected by: {client_address}")
        data = client_socket.recv(1024).decode()
        subnet = ipaddress.ip_network(data)

        # Using ThreadPoolExecutor to scan IPs concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(scan_ip, ip, 80) for ip in subnet.hosts()]

        # Wait for all scans to complete
        concurrent.futures.wait(futures)

        client_socket.sendall(data.encode())


def scan_ip(ip: str, port: int) -> None:
    """Scan IP address.

    Check if a host is up by connecting to port 80.
    
    Arguments:
        ip (str): IP address to scan.
        port (int): Port to scan.
    
    Returns:
        None: This function does not return anything.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect((str(ip), port))
            logger.debug(f"Port {port} open on ip {ip}")
    except(socket.timeout, ConnectionRefusedError):
        logger.debug(f"Port {port} closed on ip {ip}")
    except Exception as e:
        logger.debug(f"Error  scanning {ip}:{port}\n{e}")


if __name__ == "__main__":
    start_sever()