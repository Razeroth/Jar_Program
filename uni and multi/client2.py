import socket
import os

def connect_to_server(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        return client_socket
    except Exception as e:
        print(f"Error saat menghubungi server: {e}")
        return None

def send_request(client_socket, request):
    try:
        client_socket.sendall(request.encode())
        response = client_socket.recv(1024).decode()
        return response
    except Exception as e:
        print(f"Error saat mengirim/menerima data: {e}")
        return None

def unicast_chat(client_socket, username):
    while True:
        message = input("Anda: ")
        if message.lower() == "exit":
            client_socket.sendall(f"{username}: {message}".encode())
            break
        response = send_request(client_socket, f"{username}: {message}")
        print(f"Pesan dari server Unicast: {response}")

def broadcast_send_file(client_socket, file_name):
    with open(file_name, 'rb') as file:
        for data in file:
            client_socket.sendall(data)
        client_socket.sendall(b'__--END--__')
    print(f"File '{file_name}' berhasil dikirim.")

def broadcast_receive_file(client_socket, file_name):
    path_file = os.path.join("file/", file_name)
    with open(path_file, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if data == b'__--END--__':
                break
            file.write(data)

def main():
    server_ip = "localhost"
    server_port = 5000

    username = input("Masukkan username Anda: ")

    client_socket = connect_to_server(server_ip, server_port)
    if client_socket is not None:
        client_socket.sendall(username.encode())

        while True:
            print("Menu:")
            print("1. UniCast")
            print("2. MultiCast")
            print("3. BroadCast")
            print("4. Keluar")
            choice = input("Pilih fitur (1/2/3/4): ")

            if choice == "1":
                unicast_chat(client_socket, username)

            elif choice == "2":
                print("Fitur MultiCast belum diimplementasikan.")

            elif choice == "3":
                file_name = input("Masukkan nama file yang akan dikirim: ")
                client_socket.sendall(b'broadcast_send_file')
                broadcast_send_file(client_socket, file_name)

            elif choice == "4":
                print("Mengakhiri koneksi dengan server.")
                break

            else:
                print("Pilihan tidak valid. Silakan pilih lagi.")

        client_socket.close()

if __name__ == "__main__":
    start_client()
