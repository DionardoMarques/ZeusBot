import socket

def send_command(hostname, port, command):
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        client_socket.connect((hostname, port))
        
        # Send the command
        client_socket.sendall(command.encode())
        
        # Receive response (optional)
        response = client_socket.recv(1024)
        print("Response:", response.decode())
        
        # Close the connection
        client_socket.close()
        
    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")

# Usage example
hostname = 'localhost'  # Replace with the actual hostname or IP address
port = 1234  # Replace with the actual port number
command = 'IniciarRobo'

send_command(hostname, port, command)