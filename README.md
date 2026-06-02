# Python TCP SocketProgramming Chatroom

Aplikasi chatroom sederhana berbasis **TCP Socket** menggunakan Python. Mendukung banyak pengguna secara bersamaan dengan sistem broadcast pesan real-time.

---

## Struktur File

```
├── server.py   # Server chatroom (jalankan lebih dulu)
└── client.py   # Client untuk bergabung ke chatroom
```

---

## Cara Penggunaan

### 1. Jalankan Server

```bash
python server.py
```

### 2. Jalankan Client

```bash
# Default (terhubung ke localhost)
python client.py

# Custom host & port
python client.py 192.168.1.10 9999
```

Setelah terhubung, masukkan nama pengguna saat diminta, lalu mulai chatting.

### 3. Keluar dari Chatroom

tekan `Ctrl+C`.


