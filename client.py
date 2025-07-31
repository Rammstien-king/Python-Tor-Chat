import socket
import socks
from cryptography.fernet import Fernet
import threading
from meta_ai_api import MetaAI


api = MetaAI() #Meta AI object
fernet = Fernet('KHBYrz6d77qr2D8sb4wiPF09qOFhuQVP7vht28I-ZRk=')  #encryption key

class Style():
  RED = "\033[31m"
  GREEN = "\033[32m"
  BLUE = "\033[34m"
  RESET = "\033[0m"

def recv_client(client_socket,):  #recieve message
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()
        decrypted_data = fernet.decrypt(data).decode('utf-8')
        if not data:
            break
        print(f"{Style.RED}{decrypted_data}{Style.RESET}")
    

def send_client(client_socket): #send message
    while True:
        # Send a response back to the client
        message = input()
        if message == "###":
            client_socket.send(fernet.encrypt(message.encode()))
            print("You have summoned AI. Ask:")
            message = input()
            client_socket.send(fernet.encrypt(message.encode()))
        else:
            client_socket.send(fernet.encrypt(message.encode()))

def start_client():  #start client
    
    #key = Fernet.generate_key()

    print("connecting...")
    # Create a socket object
    #client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.set_default_proxy(socks.SOCKS5,"127.0.0.1", 9150)
    socket.socket = socks.socksocket
    client_socket = socket.socket()
    # Get the server address and port
    host = 'tpsyqgfdio25qxfakdksdyioq6u6bghipd3pcpboibwiowcvs3yv4gad.onion'  # Server's IP address
    port = 80

    # Connect to the server
    client_socket.connect((host, port))
    print(f"{Style.BLUE}***Connected***{Style.RESET}")
    thread_1 = threading.Thread(target=recv_client, args=(client_socket,))
    thread_2 = threading.Thread(target=send_client, args=(client_socket,))
     
    #Starting Threads
    thread_1.start()
    thread_2.start()

    # Ensuring the main program waits for both threads to finish
    thread_1.join()
    thread_2.join()
    
    # Close the socket
    #client_socket.close()

if __name__ == "__main__":
    start_client()
