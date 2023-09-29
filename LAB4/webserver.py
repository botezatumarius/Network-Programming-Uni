import json
import socket
import signal
import sys
from time import sleep

fileName = 'products.json'
with open(fileName, "r") as json_file:
    products = json.load(json_file)

# Define the server's IP address and port
HOST = '127.0.0.1'  # IP address to bind to (localhost)
PORT = 8080  # Port to listen on
# Create a socket that uses IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the address and port
server_socket.bind((HOST, PORT))
# Listen for incoming connections
server_socket.listen(5)  # Backlog for multiple simultaneous connections
print(f"Server is listening on {HOST}:{PORT}")
# Function to handle Ctrl+C and other signals


def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)
# Function to handle client requests
productNumber = 0


def handle_request(client_socket):
    # Receive and print the client's request data
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")
    # Parse the request to get the HTTP method and path
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    method = request_line[0]
    path = request_line[1]
    # Initialize the response content and status code
    response_content = ''
    status_code = 200
    # Define a simple routing mechanism
    if path == '/':
        # sleep(15)
        response_content = 'Home page'
    elif path == '/about':
        response_content = 'About page'
    elif path == '/contacts':
        response_content = 'Contacts page'
    elif path == '/products':
        productList = """
        <h1>Product list </h1>
        <a href="http://127.0.0.1:8080/products/0">Fluent Python: Clear, Concise, and Effective Programming</a><br>
        <a href="http://127.0.0.1:8080/products/1">Introducing Python: Modern Computing in Simple Packages</a>
        """
        response_content = productList
    elif '/products' in path:
        productNumber = -1
        for product in products:
            productNumber += 1
            if path == '/products' + '/' + str(productNumber):
                name = product.get("name")
                author = product.get("author")
                price = product.get("price")
                description = product.get("description")
                productTemplate = f"""Product number: {productNumber+1 if productNumber != -1 else ""}<br>
                Name: {name}<br>
                Author: {author}<br>
                Price: {price if price != -1 else ""}<br>
                Description: {description}"""
                response_content = productTemplate
                break
            else:
                response_content = '404 Not Found'
                status_code = 404
    else:
        response_content = '404 Not Found'
        status_code = 404
    # Prepare the HTTP response
    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))
    # Close the client socket
    client_socket.close()


while True:
    # Accept incoming client connections
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    try:
        # Handle the client's request in a separate thread
        handle_request(client_socket)
    except KeyboardInterrupt:
        # Handle Ctrl+C interruption here (if needed)
        pass
