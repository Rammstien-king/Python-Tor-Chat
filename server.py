import socket
from cryptography.fernet import Fernet
import threading
from meta_ai_api import MetaAI


api = MetaAI() #Meta AI object
fernet = Fernet('KHBYrz6d77qr2D8sb4wiPF09qOFhuQVP7vht28I-ZRk=')  #encryption key

class Style():     #text Color class 
  RED = "\033[31m"
  GREEN = "\033[32m"
  BLUE = "\033[34m"
  RESET = "\033[0m"

def recv_client(client_socket,):    #recieve message
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()
        decrypted_data = fernet.decrypt(data).decode('utf-8')
        if decrypted_data == "###":  # this if statement handles client queries with AI
            data = client_socket.recv(1024).decode()
            decrypted_data = fernet.decrypt(data).decode('utf-8') #recieved client Query for AI
            print("AI summoned: Question Asked: " + decrypted_data)
            message_small_reply = decrypted_data + "(Please give short answer)" #Ask AI to generate small answer only
            response = api.prompt(message=message_small_reply)
            response_send = "META AI: "+ response['message']

            print(f"{Style.GREEN}{response_send}{Style.RESET}")
            client_socket.send(fernet.encrypt(response_send.encode()))
        else:
            print(f"{Style.RED}{decrypted_data}{Style.RESET}")
        if not data:
            break
        
    

def send_client(client_socket):   #send message
    while True:
        # Send a response back to the client
        message = input()
        if message == "###":  # this if statement handles server queries with AI
            print("You have summoned AI. Ask:")
            message = input()
            AI_notify = "AI summoned: Question Asked: " + message
            client_socket.send(fernet.encrypt(AI_notify.encode()))  #server query with AI notified to client
            message_small_reply = message + "(Please give short answer)" #Ask AI to generate small answer only
            response = api.prompt(message=message_small_reply)
            response_send = "META AI: "+ response['message'] 

            print(f"{Style.GREEN}{response_send}{Style.RESET}")
            client_socket.send(fernet.encrypt(response_send.encode()))
        else:
            client_socket.send(fernet.encrypt(message.encode()))
    

def start_server():  #start server
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
