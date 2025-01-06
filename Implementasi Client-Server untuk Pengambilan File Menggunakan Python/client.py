import socket
import webbrowser

# Server configuration
SERVER_HOST = '127.0.0.1'  # Server IP address
SERVER_PORT = 12345  # Server port number

# File to request from the server
file_name = input('Enter the file name: ')

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Send the file name to the server
    client_socket.sendall(file_name.encode())

    # Receive the file data from the server
    file_data = client_socket.recv(1024)

    if file_data == b'File not found':
        print('404 File not found on the server')
        # Display a 404 Not Found message in the web browser
        html_content = '<h1>404 Not Found</h1>'
        with open('404.html', 'w') as html_file:
            html_file.write(html_content)
        webbrowser.open('404.html')

    else:
        # Save the file
        with open(file_name, 'wb') as file:
            file.write(file_data)
        print('200 OK')
        print(format(file_name),'received from the server')

        # Open the file in the web browser
        webbrowser.open(file_name)

except ConnectionRefusedError:
    print('Unable to connect to the server')

finally:
    # Close the socket
    client_socket.close()
