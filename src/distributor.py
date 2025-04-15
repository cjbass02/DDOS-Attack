import socket
import threading

# This function will distribute the connections to different servers (simulating a load balancer)
def distribute_requests(server_ips):
    """Distributes requests from clients to multiple servers."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        for ip in server_ips:
            try:
                client_socket.connect((ip, 8080))
                print(f"Request sent to server {ip}")
            except Exception as e:
                print(f"Failed to connect to server {ip}: {e}")

if __name__ == "__main__":
    servers = ["127.0.0.1", "192.168.1.2"]  # Replace with actual server IPs
    distribute_requests(servers)
