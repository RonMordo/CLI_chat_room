import socket

c = socket.socket()

c.connect(('localhost',12345))

name = input("Enter your name\n")

c.send(name.encode('ascii'))

print(c.recv(1024).decode)
