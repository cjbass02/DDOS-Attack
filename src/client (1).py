import socket

def get_server_info():
    """
    Connects to the distributor at port 5000,
    receives the server info in the form "host:port",
    and returns the parsed host and port.
    """
    distributor_address = ('127.0.0.1', 5000)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dist_socket:
        try:
            dist_socket.connect(distributor_address)
            server_info = dist_socket.recv(1024).decode().strip()
            if not server_info:
                raise ValueError("No server info received.")
            print(f"[Client] Received server info: {server_info}")
        except Exception as e:
            print(f"[Client] Failed to get server info: {e}")
            return None, None
    # Parse the info assuming it's in the form "host:port"
    host, port_str = server_info.split(":")
    return host, int(port_str)

def main():
    # Connect to the distributor to get the server assignment
    host, port = get_server_info()
    if host is None or port is None:
        return

    print(f"[Client] Connecting to server at {host}:{port}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            # Receive the greeting from the assigned server
            greeting = client_socket.recv(1024).decode().strip()
            print(f"[Client] Received from server: {greeting}")
        except Exception as e:
            print(f"[Client] Connection to server failed: {e}")

if __name__ == "__main__":
    main()
