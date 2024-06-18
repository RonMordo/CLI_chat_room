# 🗨️ CLI Chat Room

Welcome to the CLI Chat Room project! This project demonstrates a simple chat application that runs in the command line. It uses socket programming, threading, and server-client architecture to allow multiple users to chat in real-time.

## Features

- Create and join chat rooms
- List available chat rooms
- Send and receive messages in real-time
- Leave chat rooms

## Technologies Used

- Python
- Socket Programming
- Threads

## How It Works

### Socket Programming 🧩

The chat application uses sockets to enable communication between the server and clients. Sockets allow for the exchange of data over a network using TCP/IP protocols.

### Threads 🧵

To handle multiple clients simultaneously, the server uses threading. Each client connection is handled in a separate thread, allowing multiple clients to interact with the server without interfering with each other.

### Server-Client Architecture 🖥️🔗

The application follows a server-client architecture. The server manages chat rooms and client connections, while the clients connect to the server to join or create chat rooms, send messages, and receive updates.
