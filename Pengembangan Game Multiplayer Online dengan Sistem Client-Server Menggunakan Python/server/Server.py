import socket
import threading

clients = []
choices = []
clients_lock = threading.Lock()

def rps_game(c1_choice, c2_choice):
    if c1_choice == c2_choice:
        return "Draw"
    elif (c1_choice == "Rock" and c2_choice == "Scissors") or \
            (c1_choice == "Scissors" and c2_choice == "Paper") or \
            (c1_choice == "Paper" and c2_choice == "Rock"):
        return "Client 1 Wins"
    else:
        return "Client 2 Wins"

def handle_client(conn, addr):
    global choices
    print(f"[NEW CONNECTION] {addr} connected.")

    choice = conn.recv(1024).decode('utf-8')
    with clients_lock:
        choices.append((addr, choice))
        print(f"[CHOICE] Client {addr} chose {choice}")

    while len(choices) < 2:
        continue

    with clients_lock:
        c1_addr, c1_choice = choices[0]
        c2_addr, c2_choice = choices[1]
        result = rps_game(c1_choice, c2_choice)
        print(f"[RESULT] {result}")

        for client in clients:
            if client.fileno() != -1:
                try:
                    client.sendall(result.encode('utf-8'))
                except Exception as e:
                    print(f"Error sending data to {client}: {e}")

    conn.close()
    with clients_lock:
        clients.remove(conn)

def get_server_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP

def start_server():
    server_ip = get_server_ip()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, 55551))
    server.listen(2)

    print(f"[SERVER IP] The server IP is: {server_ip}")

    while len(clients) < 2:
        conn, addr = server.accept()
        with clients_lock:
            clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

    print(f"[STARTING] Game starting with {len(clients)} players.")

if __name__ == "__main__":
    start_server()
