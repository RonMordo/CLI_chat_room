import os
import socket
import threading

s = socket.socket()
print('Socket Created')

s.bind(('0.0.0.0',9999))

s.listen(3)

print('Waiting for connections')

while True:
    c, addr = s.accept()

    name = c.recv(1024).decode()

    print("Connected with ", addr, name)

    c.send(bytes(f'welcome {name}','utf-8'))

    c.close()