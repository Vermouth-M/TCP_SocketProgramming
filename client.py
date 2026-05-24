import socket
import threading
import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999

def receive_messages(client_socket):
    """Thread untuk menerima pesan dari server"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("\n[INFO] Koneksi ke server terputus.")
                break
            print(message)
        except ConnectionResetError:
            print("\n[INFO] Server menutup koneksi.")
            break
        except OSError:
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[CLIENT] Terhubung ke server {SERVER_HOST}:{SERVER_PORT}")
    except ConnectionRefusedError:
        print(f"[ERROR] Tidak bisa terhubung ke server {SERVER_HOST}:{SERVER_PORT}")
        print("[ERROR] Pastikan server sudah berjalan terlebih dahulu.")
        sys.exit(1)

    # Terima prompt nama dari server
    try:
        prompt = client_socket.recv(1024).decode('utf-8')
        name = input(prompt).strip()
        while not name:
            name = input("Nama tidak boleh kosong. Masukkan nama Anda: ").strip()
        client_socket.send(name.encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] {e}")
        client_socket.close()
        sys.exit(1)

    # Terima pesan sambutan
    welcome = client_socket.recv(1024).decode('utf-8')
    print(welcome.strip())
    print("-" * 40)
    print("Ketik pesan dan tekan Enter untuk mengirim.")
    print("Ketik 'exit' atau tekan Ctrl+C untuk keluar.")
    print("-" * 40)
    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    recv_thread.start()

    # Loop pengiriman pesan
    try:
        while True:
            message = input()
            if message.lower() == 'exit':
                print("[INFO] Keluar dari chatroom...")
                break
            if message.strip():
                formatted = f"{name} = {message}"
                print(formatted)
                client_socket.send(formatted.encode('utf-8'))
    except KeyboardInterrupt:
        print("\n[INFO] Keluar dari chatroom...")
    finally:
        client_socket.close()


if __name__ == "__main__":
    # Opsional: bisa passing host/port lewat argumen
    if len(sys.argv) >= 2:
        SERVER_HOST = sys.argv[1]
    if len(sys.argv) >= 3:
        SERVER_PORT = int(sys.argv[2])

    start_client()