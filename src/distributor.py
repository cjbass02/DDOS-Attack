import socket
import threading

# List of available servers (all assumed to be on localhost, ports 5001–5010)
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

# Dictionary to track connection attempts by IP
connection_attempts = {}
attempt_lock = threading.Lock()

# Threshold for blacklisting
BLACKLIST_THRESHOLD = 10

def handle_client(conn, addr):
    global server_index, connection_attempts
    client_ip = addr[0]
    
    # Update connection attempt count safely
    with attempt_lock:
        count = connection_attempts.get(client_ip, 0) + 1
        connection_attempts[client_ip] = count
    print(f"[Distributor] Connection from {client_ip}. Attempt count: {count}")

    # If the client has reached the threshold, block the connection
    if count >= BLACKLIST_THRESHOLD:
        print(f"[Distributor] Blocking connection from {client_ip} after {count} attempts.")
        try:
            conn.sendall("Your IP has been blacklisted due to excessive connection attempts.".encode())
        except Exception as e:
            print(f"[Distributor] Error sending block notification to {client_ip}: {e}")
        finally:
            conn.close()
        return

    # For allowed IPs, do a round-robin assignment to one of the servers
    assigned_server = servers[server_index % len(servers)]
    server_index += 1

    server_info = f"{assigned_server[0]}:{assigned_server[1]}"
    try:
        conn.sendall(server_info.encode())
        print(f"[Distributor] Assigned {server_info} to client {client_ip}")
    except Exception as e:
        print(f"[Distributor] Failed to send server info to {client_ip}: {e}")
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
