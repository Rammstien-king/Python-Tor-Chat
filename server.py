import socket
from cryptography.fernet import Fernet
import threading

fernet = Fernet('KHBYrz6d77qr2D8sb4wiPF09qOFhuQVP7vht28I-ZRk=')
class Style():
  RED = "\033[31m"
  GREEN = "\033[32m"
  BLUE = "\033[34m"
  RESET = "\033[0m"

def recv_client(client_socket,):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()
        decrypted_data = fernet.decrypt(data).decode('utf-8')
        if not data:
            break
        print(f"{Style.RED}{decrypted_data}{Style.RESET}")
    

def send_client(client_socket):
    while True:
        # Send a response back to the client
        message = input()
        client_socket.send(fernet.encrypt(message.encode()))
    

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name and port
    host = '127.0.0.1'  # Localhost
    port = 80

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Enable the server to accept connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")
    

    
    # Accept a connection from a client
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    thread_1 = threading.Thread(target=recv_client, args=(client_socket,))
    thread_2 = threading.Thread(target=send_client, args=(client_socket,))
     
    #Starting Threads
    thread_1.start()
    thread_2.start()

    # Ensuring the main program waits for both threads to finish
    thread_1.join()
    thread_2.join()
    # Close the sockets
    #client_socket.close()
    #server_socket.close()

if __name__ == "__main__":
    start_server()