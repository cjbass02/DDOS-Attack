import socket
import threading
import time

DISTRIBUTOR_ADDRESS = ('127.0.0.1', 5000)

def simulate_client(client_id):
    """
    This function simulates a single client attempting to connect to the distributor.
    Each client receives server information and then closes the connection.
    """
    try:
        # Create and configure a new socket for this client connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dist_socket:
            dist_socket.settimeout(5)  # set a timeout to prevent hanging
            dist_socket.connect(DISTRIBUTOR_ADDRESS)
            
            # Receive the server assignment (expected in "host:port" format)
            server_info = dist_socket.recv(1024).decode().strip()
            print(f"[Client {client_id}] Received server info: {server_info}")
    except Exception as e:
        print(f"[Client {client_id}] Connection failed: {e}")

def main():
    """
    In the main loop, a new client thread is spawned every second.
    This loop simulates a low-intensity DDoS attack where each client individually connects to the distributor.
    """
    client_id = 0
    while True:
        client_id += 1
        # Start a new thread representing a new client connection
        t = threading.Thread(target=simulate_client, args=(client_id,))
        t.daemon = True  # Allow threads to be cleaned up on program exit
        t.start()
        # Wait one second before spawning the next client
        time.sleep(1)

if __name__ == "__main__":
    try:
        print("Starting DDoS simulation of distributor connection. Press Ctrl+C to stop.")
        main()
    except KeyboardInterrupt:
        print("DDoS simulation stopped.")
