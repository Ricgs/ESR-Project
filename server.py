import socket
import threading

HOST = "10.0.0.10"
PORT = 5000

def handle_client(conn, addr):
    with conn:
        print(f"Ligação de {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Recebido:", data.decode())
            conn.sendall(b"HELLO from server")
            

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor ativo em {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()