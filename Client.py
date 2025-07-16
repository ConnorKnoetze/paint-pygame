import socket
import threading

class Port:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self, target_host, target_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((target_host, target_port))
        return self.sock


def receive_messages(sock, recv_messages, lock):
    while True:
        try:
            data = sock.recv(8192)
            if not data:
                print("Connection closed by server.")
                break
            with lock:
                recv_messages.append(data.decode())
        except socket.error as e:
            print(f"Error receiving data: {e}")
            break

def send_message(message, sock):
    try:
        sock.sendall(message.encode())
    except socket.error as e:
        print(f"Error sending message: {e}")

def main():
    server = "127.0.0.1"
    portid = 5000

    port = Port()
    sock = port.connect(server, portid)
    sock.sendall("Connor".encode())

if __name__ == "__main__":
    main()