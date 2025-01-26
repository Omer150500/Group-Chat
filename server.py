import socket
import threading

HOST = '127.0.0.1'  # כתובת ה-IP של השרת
PORT = 50001        # הפורט שעליו השרת מאזין

connected_clients = {}  # רשימת לקוחות מחוברים: {שם: סוקט}

def handle_client(client_socket, client_address):
    try:
        # בקשת שם המשתמש
        client_socket.sendall("Welcome to the chat! Please enter your name:\n".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()

        # הוספת המשתמש לרשימת המחוברים
        connected_clients[username] = client_socket
        print(f"{username} connected from {client_address}")

        # שליחת רשימת משתמשים מחוברים ללקוח
        client_socket.sendall(f"Currently connected users: {', '.join(connected_clients.keys())}\n".encode('utf-8'))

        # לולאת קבלת הודעות מהלקוח
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            # אם ההודעה מתחילה ב-"/", זו הודעה שנשלחת למישהו ספציפי
            if message.startswith("/"):
                parts = message[1:].split(" ", 1)
                if len(parts) == 2:
                    target_username, message_to_send = parts
                    if target_username in connected_clients:
                        target_socket = connected_clients[target_username]
                        target_socket.sendall(f"Private message from {username}: {message_to_send}\n".encode('utf-8'))
                    else:
                        client_socket.sendall(f"User {target_username} not found.\n".encode('utf-8'))
                else:
                    client_socket.sendall("Usage: /<username> <message>\n".encode('utf-8'))
            else:
                # שליחת ההודעה לכולם
                print(f"{username}: {message}")
                for client in connected_clients.values():
                    client.sendall(f"{username}: {message}\n".encode('utf-8'))

    except ConnectionResetError:
        print(f"Connection with {username} lost.")
    finally:
        # סגירת החיבור וניקוי המשתמש מהרשימה
        print(f"{username} disconnected.")
        del connected_clients[username]
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()
