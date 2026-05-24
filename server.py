import socket
import threading

HOST = '0.0.0.0'
PORT = 9999

clients = {}  # socket -> name
lock = threading.Lock()

def broadcast(message, sender_socket=None):
    with lock:
        for client_socket in list(clients.keys()):
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    client_socket.close()
                    del clients[client_socket]

def handle_client(client_socket, client_address):
    ip, port = client_address
    print(f"[+] Koneksi baru dari {ip}:{port}")

    try:
        # Minta nama client
        client_socket.send("Masukkan nama Anda: ".encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8').strip()

        if not name:
            name = f"User_{port}"

        with lock:
            clients[client_socket] = name

        print(f"[+] {name} ({ip}:{port}) telah bergabung")
        client_socket.send(f"Selamat Datang di Chatroom, {name}!\n".encode('utf-8'))

        join_msg = f"[SERVER] {name} telah bergabung ke chatroom!"
        broadcast(join_msg, client_socket)
        print(f"[BROADCAST] {join_msg}")

        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8').strip()
                if not message:
                    break

                full_msg = f"[{name}] {message}"
                print(f"[MSG] {full_msg}")
                broadcast(full_msg, client_socket)

            except ConnectionResetError:
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                break

    except Exception as e:
        print(f"[ERROR] handle_client: {e}")
    finally:
        with lock:
            name = clients.pop(client_socket, f"{ip}:{port}")
        client_socket.close()

        leave_msg = f"[SERVER] {name} telah meninggalkan chatroom."
        broadcast(leave_msg)
        print(f"[INFO] {leave_msg}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)
    print(f"[SERVER] Chat server berjalan di {HOST}:{PORT}")
    print(f"[SERVER] Menunggu koneksi client...\n")

    try:
        while True:
            client_socket, client_address = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Server dihentikan.")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()