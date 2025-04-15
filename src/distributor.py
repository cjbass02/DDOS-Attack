import socket
import threading

# List of available servers (assuming all are on localhost and using ports 5001–5010)
servers = [
    ("127.0.0.1", 5001),
    ("127.0.0.1", 5002),
    ("127.0.0.1", 5003),
    ("127.0.0.1", 5004),
    ("127.0.0.1", 5005),
    ("127.0.0.1", 5006),
    ("127.0.0.1", 5007),
    ("127.0.0.1", 5008),
    ("127.0.0.1", 5009),
    ("127.0.0.1", 5010)
]

server_index = 0  # To implement round-robin assignment

def handle_client(conn, addr):
    global server_index
    print(f"[Distributor] Received connection from {addr}")
    
    # Round-robin: assign the next server in the list
    assigned_server = servers[server_index % len(servers)]
    server_index += 1

    # Format the assigned server's info as "host:port"
    server_info = f"{assigned_server[0]}:{assigned_server[1]}"
    try:
        conn.sendall(server_info.encode())
        print(f"[Distributor] Assigned {server_info} to client {addr}")
    except Exception as e:
        print(f"[Distributor] Failed to send server info to {addr}: {e}")
    finally:
        conn.close()

def main():
    distributor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        distributor_socket.bind(('0.0.0.0', 5000))
    except Exception as e:
        print(f"[Distributor] Failed to bind on port 5000: {e}")
        return
    distributor_socket.listen(5)
    print("[Distributor] Listening on port 5000...")
    
    while True:
        conn, addr = distributor_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    main()
