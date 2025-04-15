import socket
import threading

# Maximum number of allowed connections
MAX_CONNECTIONS = 5
BLOCKED_IPS = set()

def handle_client(client_socket, addr):
    """Handles the incoming client request."""
    print(f"Connection from {addr}")
    # Simulate some work or interaction with the client
    client_socket.send("Welcome to the server!".encode())
    client_socket.close()

def server_program():
    """Sets up the server and listens for incoming connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(MAX_CONNECTIONS)

    print("Server listening on port 8080...")

    while True:
        client_socket, addr = server_socket.accept()

        if addr[0] in BLOCKED_IPS:
            print(f"Blocked IP attempted to connect: {addr}")
            client_socket.close()
            continue
        
        # Create a thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    server_program()
