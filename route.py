import socket
import time



def check_neighbor(ip,port=5000):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.sendall(b"GET_NEIGHBORS")
        data = s.recv(1024)
        print(f"[CONTROL] Vizinhos do nó {ip}:{port} -> {data.decode()}")
        s.close()
    except Exception as e:
        print(f"[CONTROL] Erro ao contactar {ip}:{port}: {e}")
    

def route_finder():
    None



