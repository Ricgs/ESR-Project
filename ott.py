import socket
import threading
import argparse
import time

neighbors_list = []


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def server_thread(port):
    def handle_client(conn, addr):
        with conn:
            print(f"[SERVER] Ligação recebida de {addr}")
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"[SERVER] Recebido de {addr}: {data.decode()}")
                    conn.sendall(f"HELLO_ACK from {get_local_ip()}".encode())
                except Exception as e:
                    print(f"[SERVER] Erro com {addr}: {e}")
                    break

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen()
    print(f"[SERVER] Nó overlay ativo na porta {port}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


def connect_to_neighbors(neighbors, retry_interval=5):
    while True:
        for neighbor in neighbors:
            ip, port = neighbor.split(':')
            port = int(port)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((ip, port))
                print(f"[CLIENT] Ligado a {ip}:{port}")
                s.sendall(f"HELLO from {get_local_ip()}".encode())
                data = s.recv(1024)
                print(f"[CLIENT] Resposta de {ip}:{port}: {data.decode()}")
                s.close()
            except Exception as e:
                print(f"[CLIENT] Falha ao ligar a {ip}:{port} ({e}). Nova tentativa em {retry_interval}s.")
        time.sleep(retry_interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nó overlay OTT")
    parser.add_argument('--port', type=int, required=True, help='Porta do servidor do nó')
    parser.add_argument('--neighbors', nargs='*', default=[], help='Lista de vizinhos ip:port')
    args = parser.parse_args()

    # Inicia o servidor numa thread separada
    threading.Thread(target=server_thread, args=(args.port,), daemon=True).start()

    # Dá tempo para o servidor iniciar
    time.sleep(1)

    # Liga aos vizinhos (se houver)
    if args.neighbors:
        threading.Thread(target=connect_to_neighbors, args=(args.neighbors,), daemon=True).start()


    # Mantém o programa ativo indefinidamente
    print("[SYSTEM] Nó ativo. A aguardar mensagens... (Ctrl+C para sair)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SYSTEM] Encerrado pelo utilizador.")
