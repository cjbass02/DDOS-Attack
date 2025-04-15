import socket
import threading
import sys

DISTRIBUTOR_ADDRESS = ('192.168.40.196', 5000)
BLACKLIST_MESSAGE = "BLACKLISTED: Your IP has exceeded the connection attempt limit."

def chat_session(server_socket):
    print("[Client] Connected to messaging server. You can start chatting. Type 'exit' to disconnect.")
    
    stop_event = threading.Event()

    def receive_messages():
        while not stop_event.is_set():
            try:
                data = server_socket.recv(1024)
                if not data:
                    print("\n[Client] Server disconnected.")
                    stop_event.set()
                    break
                print(f"\nServer: {data.decode().strip()}\nYou: ", end='', flush=True)
            except Exception as e:
                print(f"\n[Client] Error receiving message: {e}")
                stop_event.set()
                break

    def send_messages():
        while not stop_event.is_set():
            try:
                msg = input("You: ")
                if msg.lower() == "exit":
                    stop_event.set()
                    break
                server_socket.sendall(msg.encode())
            except Exception as e:
                print(f"[Client] Error sending message: {e}")
                stop_event.set()
                break

    recv_thread = threading.Thread(target=receive_messages, daemon=True)
    send_thread = threading.Thread(target=send_messages, daemon=True)
    recv_thread.start()
    send_thread.start()

    recv_thread.join()
    send_thread.join()
    server_socket.close()
    print("[Client] Chat session ended.")

def main():
    # Contact the distributor to obtain server assignment.
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dist_socket:
            dist_socket.settimeout(5)
            dist_socket.connect(DISTRIBUTOR_ADDRESS)
            response = dist_socket.recv(1024).decode().strip()
    except Exception as e:
        print(f"[Client] Failed to connect to the distributor: {e}")
        sys.exit(1)

    if response.startswith("BLACKLISTED"):
        print(f"[Client] {response}")
        sys.exit(0)

    # Parse the server info (format: "host:port").
    try:
        host, port_str = response.split(":")
        server_port = int(port_str)
    except Exception as e:
        print(f"[Client] Invalid server info received: {response}")
        sys.exit(1)

    print(f"[Client] Assigned to messaging server at {host}:{server_port}")

    # Connect to the assigned messaging server.
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, server_port))
    except Exception as e:
        print(f"[Client] Failed to connect to messaging server: {e}")
        sys.exit(1)

    chat_session(server_socket)

if __name__ == "__main__":
    main()
