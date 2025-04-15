import socket
import threading

# List of available messaging servers.
# These servers should be launched separately (for example, in different terminals).
servers = [
    ("192.168.40.151", 5001),
    ("192.168.40.151", 5002),
    ("192.168.40.151", 5003)
]

server_index = 0  # for round-robin assignment

# Dictionary to track connection attempts per client IP.
connection_attempts = {}
attempt_lock = threading.Lock()

MAX_ATTEMPTS = 3
BLACKLIST_MESSAGE = "BLACKLISTED: Your IP has exceeded the connection attempt limit."

def handle_client(conn, addr):
    global server_index
    client_ip = addr[0]
    
    # Update connection attempt count safely.
    with attempt_lock:
        count = connection_attempts.get(client_ip, 0) + 1
        connection_attempts[client_ip] = count
    print(f"[Distributor] {client_ip} connection attempt #{count}")

    # If the count exceeds the threshold, send the blacklist message.
    if count > MAX_ATTEMPTS:
        print(f"[Distributor] {client_ip} is blacklisted.")
        try:
            conn.sendall(BLACKLIST_MESSAGE.encode())
        except Exception as e:
            print(f"[Distributor] Error sending blacklist message: {e}")
        finally:
            conn.close()
        return

    # Otherwise, assign a server using round-robin.
    assigned_server = servers[server_index % len(servers)]
    server_index += 1
    server_info = f"{assigned_server[0]}:{assigned_server[1]}"
    try:
        conn.sendall(server_info.encode())
        print(f"[Distributor] Assigned server {server_info} to {client_ip}")
    except Exception as e:
        print(f"[Distributor] Error sending server info: {e}")
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
        try:
            conn, addr = distributor_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
        except Exception as e:
            print(f"[Distributor] Error accepting connections: {e}")

if __name__ == "__main__":
    main()
