import threading
import socket

HEADER = 64
PORT = 9999
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

rooms = {}  # Room -> List of (conn, addr)
private_rooms = set()  # Set of private room names


def send_message(conn, message):
    message = message.encode(FORMAT)
    msg_length = len(message)
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b' ' * (HEADER - len(msg_length))
    conn.send(msg_length)
    conn.send(message)


def broadcast(room, message):
    for client, addr in rooms[room]:
        send_message(client, message)


def create_room(room_name, conn, addr, private=False):
    if room_name in rooms:
        send_message(conn, f"Room {room_name} already exists.")
        return False
    else:
        rooms[room_name] = [(conn, addr)]
        private_rooms.add(room_name) if private else None
        send_message(conn, f"Room {room_name} created.")
        print(f"[ROOM CREATED] {room_name} by {addr}")
        return True


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
                elif command == "!LIST":
                    room_list = ', '.join(rooms.keys())
                    send_message(conn, f"Rooms: {room_list}")
                elif command == "!CREATE":
                    room_name = params[0]
                    private = "private" in params
                    created = create_room(room_name, conn, addr, private)
                    if created:
                        msg = "1".encode(FORMAT)
                        send_message(conn, msg)

                elif command == "!JOIN":
                    room_name = params[0]
                    if room_name in rooms:
                        rooms[room_name].append((conn, addr))
                        send_message(conn, f"Joined room {room_name}.")
                        broadcast(room_name, f"{addr} has joined the room.")
                        current_room = room_name
                    else:
                        send_message(conn, f"Room {room_name} does not exist.")
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


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()