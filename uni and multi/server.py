import socket
import threading

# Connection Data
host = '10.217.19.91'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((host, port))
except socket.error:
    print("Try to check your IP")
else:
    print("Server Connected")
    server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients or a Single Client
def broadcast(message, sender=None, recipient=None):
    if recipient:
        try:
            recipient.send(message)
        except:
            # Removing And Closing Client
            index = clients.index(recipient)
            clients.remove(recipient)
            recipient.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
    else:
        for client in clients:
            # Don't send the message back to the sender
            if client != sender:
                try:
                    client.send(message)
                except:
                    # Removing And Closing Client
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    nickname = nicknames[index]
                    broadcast('{} left!'.format(nickname).encode('ascii'))
                    nicknames.remove(nickname)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            if message:
                if message.decode('ascii').startswith('UNICAST'):
                    _, recipient, message = message.decode('ascii').split(' ', 2)
                    recipient = recipient.strip()
                    if recipient in nicknames:
                        recipient_index = nicknames.index(recipient)
                        recipient_client = clients[recipient_index]
                        broadcast(message.encode('ascii'), client, recipient_client)
                elif message.decode('ascii').startswith('MULTICAST'):
                    _, message = message.decode('ascii').split(' ', 1)
                    broadcast(message.encode('ascii'), client)
                else:
                    broadcast(message, client)
        except:
            # Removing And Closing Client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        joined_message = "{} joined!".format(nickname)
        print(joined_message)
        broadcast(joined_message.encode('ascii'), client)

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()
