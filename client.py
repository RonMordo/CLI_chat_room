import threading
import socket

HEADER = 64
PORT = 9999
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    try:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
    except BrokenPipeError:
        print("Connection closed by the server.")
        client.close()


def receive():
    while True:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                print(f"[SERVER]: {msg}")
                if msg == DISCONNECT_MESSAGE:
                    print("You are disconnected from the server.")
                    client.close()
                    break
        except ConnectionResetError:
            print("Connection lost.")
            client.close()
            break
        except Exception as e:
            print(f"Error receiving data from server: {e}")
            client.close()
            break


def main():
    thread = threading.Thread(target=receive)
    thread.start()
    in_room = None

    while True:
        if not in_room:
            print("\nOptions: [L]ist rooms, [C]reate room, [J]oin room, [Q]uit")
            option = input("Select an option: ").lower()
            if option == 'q':
                send(DISCONNECT_MESSAGE)
                break
            elif option == 'l':
                send("!LIST")
            elif option == 'c':
                room_name = input("Enter room name to create: ")
                private = input("Make it private? (yes/no): ").lower() == 'yes'
                command = f"!CREATE {room_name} {'private' if private else ''}"
                send(command)
                created = client.recv(HEADER).decode(FORMAT)
                if created:
                    in_room = created
            elif option == 'j':
                room_name = input("Enter room name to join: ")
                command = f"!JOIN {room_name}"
                send(command)


main()