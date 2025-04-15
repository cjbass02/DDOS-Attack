import socket
import threading
import sys
import select

def chat_session(conn, addr):
    print(f"[Server] Client {addr} connected. Starting chat session.")
    
    # A flag to indicate when the chat session should stop.
    stop_event = threading.Event()

    def receive_messages():
        while not stop_event.is_set():
            try:
                data = conn.recv(1024)
                if not data:
                    print("\n[Server] Client disconnected.")
                    stop_event.set()
                    break
                message = data.decode().strip()
                if message.lower() == "exit":
                    print("\n[Server] Client sent 'exit'. Ending chat session.")
                    stop_event.set()
                    break
                # Print the client's message and show a prompt.
                print(f"\nClient: {message}\nYou: ", end='', flush=True)
            except Exception as e:
                print(f"\n[Server] Error receiving message: {e}")
                stop_event.set()
                break

    def send_messages():
        # Use non-blocking input to allow periodic check of stop_event.
        
        while not stop_event.is_set():         
            ready, _, _ = select.select([sys.stdin], [], [], 1)
            if ready:
                print("You: ", end='', flush=True)
                msg = sys.stdin.readline().rstrip('\n')
                if msg.lower() == "exit":
                    # Optionally send the exit message to client.
                    try:
                        conn.sendall(msg.encode())
                    except Exception as e:
                        print(f"[Server] Error sending exit message: {e}")
                    stop_event.set()
                    break
                try:
                    conn.sendall(msg.encode())
                except Exception as e:
                    print(f"[Server] Error sending message: {e}")
                    stop_event.set()
                    break

    recv_thread = threading.Thread(target=receive_messages, daemon=True)
    send_thread = threading.Thread(target=send_messages, daemon=True)
    recv_thread.start()
    send_thread.start()

    # Wait for both threads to finish.
    recv_thread.join()
    send_thread.join()
    conn.close()
    print("[Server] Chat session ended. Waiting for next client...")

def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Port must be an integer.")
        sys.exit(1)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('0.0.0.0', port))
    except Exception as e:
        print(f"[Server] Failed to bind on port {port}: {e}")
        sys.exit(1)

    server_socket.listen(5)
    print(f"[Server] Messaging server listening on port {port}.")
    
    while True:
        try:
            conn, addr = server_socket.accept()
            chat_session(conn, addr)
        except Exception as e:
            print(f"[Server] Error accepting connections: {e}")

if __name__ == "__main__":
    main()
