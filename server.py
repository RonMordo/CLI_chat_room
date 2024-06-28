import socket
import threading
import time

# Connection Data
host = '127.0.0.1'
port = 9999

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Dictionary For Rooms
rooms = {}


MENU_MESSAGE = '!MENU'


# Sending Messages To All Connected Clients
def broadcast(message, sender):
    for room in rooms:
        if sender in rooms[room]:
            for client in rooms[room]:
                if client != sender:
                    client.send(message)


def create_room(client):
    client.send('Enter the name of the room you would like to create: '.encode('ascii'))
    room_name = client.recv(1024).decode('ascii')
    room_name = room_name.split(':')[1].strip()
    if room_name in rooms:
        client.send(f'{MENU_MESSAGE}'.encode('ascii'))
    else:
        rooms[room_name] = []
        rooms[room_name].append(client)
        client.send(f'Room {room_name} created and you have joined!'.encode('ascii'))


def join_room(client):
    client.send('Enter the name of the room you would like to join: '.encode('ascii'))
    room_name = client.recv(1024).decode('ascii')
    room_name = room_name.split(':')[1].strip()
    if room_name in rooms:
        rooms[room_name].append(client)
        client.send(f'Joined room {room_name}!'.encode('ascii'))
        broadcast(f'{nicknames[clients.index(client)]} joined the room!'.encode('ascii'), client)
    else:
        client.send(f'{MENU_MESSAGE}'.encode('ascii'))


def list_rooms(client):
    client.send('Rooms: '.encode('ascii'))
    for room in rooms:
        client.send(f'{room}, '.encode('ascii'))
    time.sleep(1)
    client.send(f'{MENU_MESSAGE}'.encode('ascii'))


def quit_program(client):
    index = clients.index(client)
    nickname = nicknames[index]
    for room in rooms:
        if client in rooms[room]:
            rooms[room].remove(client)
            broadcast(f'{nickname} left the room!'.encode('ascii'), client)
    clients.remove(client)
    client.send('You have left the server!'.encode('ascii'))
    time.sleep(1)
    client.send('!QUIT'.encode('ascii'))
    client.close()
    nicknames.remove(nickname)


def leave_room(client):
    for room in rooms:
        if client in rooms[room]:
            rooms[room].remove(client)
            broadcast(f'{nicknames[clients.index(client)]} left the room!'.encode('ascii'), client)
        client.send('You have left the room!'.encode('ascii'))
        time.sleep(1)
        client.send(f'{MENU_MESSAGE}'.encode('ascii'))


# Handling Commands From Clients
def handle_command(client, command):
    if command == '!c':
        create_room(client)
    elif command == '!j':
        join_room(client)
    elif command == '!l':
        list_rooms(client)
    elif command == '!q':
        quit_program(client)
    elif command == '!LEAVE':
        leave_room(client)
    else:
        client.send('Invalid command!'.encode('ascii'))


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            if message.decode('ascii').startswith('!'):
                handle_command(client, message.decode('ascii'))
            else:
                broadcast(message, client)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'), client)
            nicknames.remove(nickname)
            clients.remove(client)
            client.close()
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('!NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        client.send('You are connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()

