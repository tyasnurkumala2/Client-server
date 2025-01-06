import socket
import os

# Server configuration
HOST = '127.0.0.1'  # Server IP address
PORT = 12345  # Server port number
FILE_DIRECTORY = './files/'  # Directory to store files

# Create the directory if it doesn't exist
if not os.path.exists(FILE_DIRECTORY):
    os.makedirs(FILE_DIRECTORY)

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print('Server listening on {}:{}'.format(HOST, PORT))

while True:
    # Accept client connections
    client_socket, client_address = server_socket.accept()
    print('Client connected:', client_address)

    # Receive the file name from the client
    file_name = client_socket.recv(1024).decode()
    file_path = os.path.join(FILE_DIRECTORY, file_name)

    try:
        # Open the requested file
        with open(file_path, 'rb') as file:
            # Read the file contents
            file_data = file.read()

        # Send the file data to the client
        client_socket.sendall(file_data)
        print('File "{}" sent to {}'.format(file_name, client_address))

    except FileNotFoundError:
        # File not found
        client_socket.sendall(b'File not found')

    # Close the client connection
    client_socket.close()
