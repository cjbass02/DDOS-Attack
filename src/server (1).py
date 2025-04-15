import socket
import threading

def server_thread(port):
    """Starts a server that listens on the given port, sends a greeting, and then closes the connection."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('0.0.0.0', port))
    except Exception as e:
        print(f"Failed to bind server on port {port}: {e}")
        return
    server_socket.listen(5)
    print(f"[Server] Listening on port {port}...")
    
    while True:
        client, addr = server_socket.accept()
        print(f"[Server on {port}] Connection from {addr}")
        try:
            # Send a simple greeting to the client
            message = f"Hello from server on port {port}!"
            client.sendall(message.encode())
        except Exception as e:
            print(f"[Server on {port}] Error sending data: {e}")
        finally:
            client.close()

if __name__ == "__main__":
    # Launch 10 servers on ports 5001 to 5010
    ports = range(5001, 5011)
    threads = []
    for port in ports:
        t = threading.Thread(target=server_thread, args=(port,))
        t.daemon = True  # Make threads exit when the main program does
        t.start()
        threads.append(t)
    
    print("[Server] All servers are running. Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[Server] Shutting down.")
