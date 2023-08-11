import socket
import threading
import os
import sys

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('10.217.19.91', 55555))

# Variable to keep track of whether "Server is Connected" message has been displayed or not
connected_message_displayed = False

# Listening to Server and Sending Nickname
def receive():
    global connected_message_displayed
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024)
            if message[:4].decode('ascii') == 'NICK':
                client.send(nickname.encode('ascii'))
                # Clear screen and print "Server is Connected"
                if not connected_message_displayed:
                    clear_screen()
                    print("Server is Connected")
                    print("                   ")
                    print("#Typing and ENTER to SEND a Message")
                    print("                   ")
                    connected_message_displayed = True
            else:
                print(message.decode('ascii'))
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break

# Clearing the Screen
def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Function to send Unicast or Multicast messages
def send_message():
    while True:
        print("TerminalChat")
        print("1. UniCast")
        print("2. MultiCast")
        choice = input("Enter your choice: ")

        if choice == '1':
            recipient = input("Enter the recipient's nickname: ")
            message = input("Enter your message: ")
            full_message = f"UNICAST {recipient} {message}"
            client.send(full_message.encode('ascii'))
        elif choice == '2':
            message = input("Enter your multicast message: ")
            full_message = f"MULTICAST {message}"
            client.send(full_message.encode('ascii'))
        else:
            print("Invalid choice. Try again.")

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=send_message)
write_thread.start()

# Main loop to keep the threads running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nExited.")
    sys.exit()
