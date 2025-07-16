import socket
import threading
import keyboard

clients = {}

def handle_keypress():
    if keyboard.is_pressed("ctrl+c"):
        raise KeyboardInterrupt

def handle_client(client_sock, client_addr):
    if client_addr not in clients:
        clients[client_addr] = client_sock
    print(f"Client {client_addr} connected.")
    try:
        while True:
            data = client_sock.recv(8192)
            if not data:
                print(f"Client {client_addr} disconnected.")
                break
            else:
                for client in clients:
                    if client != client_addr:
                        clients[client].sendall(data)


    except Exception as e:
        print(f"Error handling client {client_addr}: {e}")
    client_sock.close()

def main():
    host = '0.0.0.0'
    port = 5000
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(10)
    server_sock.settimeout(1.0)
    print(f"Server listening on {host}:{port}")
    try:
        while True:
            try:
                client_sock, client_addr = server_sock.accept()
                t = threading.Thread(target=handle_client, args=(client_sock, client_addr), daemon=True)
                t.start()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()