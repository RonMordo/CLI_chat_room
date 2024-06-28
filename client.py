import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))


input_lock = threading.Lock()
input_priority = True


# Menu
def menu(connected=False):
    global input_priority
    with input_lock:
        if input_priority:
            command = "!" + input("Would you like to [C]reate a room, [J]oin a room, [L]ist rooms, or [Q]uit? ").lower()
            client.send(command.encode('ascii'))
            input_priority = False
    if not connected:
        write()


# Listening to Server and Sending Nickname
def receive():
    global input_priority
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == '!NICK':
                client.send(nickname.encode('ascii'))
            elif message == '!MENU':
                input_priority = True
                menu(True)
            elif message == '!QUIT':
                print("Quitting...")
                client.close()
                break
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break


# Sending Messages To Server
def write():
    global input_priority
    while True:
        with input_lock:
            if not input_priority:
                message = input('')
                if message.startswith('!'):
                    client.send(message.encode('ascii'))
                else:
                    message = '{}: {}'.format(nickname, message)
                    client.send(message.encode('ascii'))


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=menu)
write_thread.start()

