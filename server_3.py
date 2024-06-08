import socket
import threading

HEADER = 64
PORT = 9999
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
LIST_COMMAND = "!LIST"
CREATE_COMMAND = "!CREATE"
JOIN_COMMAND = "!JOIN"
MAX_CLIENTS_PER_ROOM = 10  # Set max number of clients per room

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

rooms = {}  # Room -> List of (conn, addr)
private_rooms = set()  # Set of private room names

def send_message(conn, message):
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    current_room = None

    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                command, *params = msg.split()
                if command == DISCONNECT_MESSAGE:
                    connected = False
                    if current_room:
                        rooms[current_room].remove((conn, addr))
                        broadcast(current_room, f"{addr} has left the room.")
                elif command == LIST_COMMAND:
                    list_rooms(conn)
                elif command == CREATE_COMMAND:
                    room_name = params[0]
                    private = "private" in params
                    create_room(room_name, conn, addr, private)
                elif command == JOIN_COMMAND:
                    room_name = params[0]
                    join_room(room_name, conn, addr)
                    current_room = room_name if room_name in rooms else None
                else:
                    if current_room:
                        broadcast(current_room, f"[{addr}] {msg}")
                    else:
                        send_message(conn, "You are not in a room. Join or create one first.")
        except ConnectionResetError:
            connected = False
            if current_room and (conn, addr) in rooms.get(current_room, []):
                rooms[current_room].remove((conn, addr))
                broadcast(current_room, f"{addr} has left the room.")
            conn.close()
            break
        except Exception as e:
            print(f"Error: {e}")
            connected = False
            if current_room and (conn, addr) in rooms.get(current_room, []):
                rooms[current_room].remove((conn, addr))
                broadcast(current_room, f"{addr} has left the room.")
            conn.close()
            break

def list_rooms(conn):
    available_rooms = [room for room in rooms if room not in private_rooms]
    room_list = "Available rooms: " + ", ".join(available_rooms) if available_rooms else "No public rooms available."
    send_message(conn, room_list)

def create_room(room_name, conn, addr, private=False):
    if room_name in rooms:
        send_message(conn, f"Room '{room_name}' already exists.")
    else:
        rooms[room_name] = [(conn, addr)]
        if private:
            private_rooms.add(room_name)
        send_message(conn, f"Room '{room_name}' created and you have joined it.")

def join_room(room_name, conn, addr):
    def join_room(room_name, conn, addr):
        if room_name in rooms:
            if any(client_addr == addr for _, client_addr in rooms[room_name]):
                send_message(conn, "You are already in this room.")
            elif len(rooms[room_name]) < MAX_CLIENTS_PER_ROOM:
                rooms[room_name].append((conn, addr))
                broadcast(room_name, f"{addr} has joined the room '{room_name}'.")
                send_message(conn, f"You have joined the room '{room_name}'.")
            else:
                send_message(conn, "Room is full.")
        else:
            send_message(conn, "Room does not exist.")

def broadcast(room, message):
    for conn, _ in rooms[room]:
        try:
            send_message(conn, message)
        except BrokenPipeError:
            pass  # Handle broken pipe error by continuing

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()
