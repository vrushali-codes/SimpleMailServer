import socket
import os
import mimetypes
from datetime import datetime
from threading import Thread
import smtplib
from urllib.parse import urlparse, parse_qs

# Server configuration
HOST = '127.0.0.1'
PORT = 8081
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMAIL_ADDRESS = "my_email"
EMAIL_PASSWORD = "my_password"

# Generate HTTP response
def generate_response(status_code, body, content_type="text/html"):
    response = f"HTTP/1.1 {status_code}\n"
    response += f"Content-Type: {content_type}\n"
    response += f"Content-Length: {len(body.encode('utf-8'))}\n\n"
    response += body
    return response

# Handle routes and requests
def handle_request(request):
    try:
        request_line = request.splitlines()[0]
        method, path, _ = request_line.split()

        log_request(method, path)

        # Serve static files
        if path == '/':
            path = '/index.html'
        file_path = os.path.join(BASE_DIR, path.lstrip('/'))
        if os.path.isfile(file_path):
            content_type, _ = mimetypes.guess_type(file_path)
            with open(file_path, 'r') as file:
                content = file.read()
            return generate_response("200 OK", content, content_type or "text/html")

        # Email route
        if path.startswith('/send-email'):
            return handle_send_email(path)

        # File not found
        return generate_response("404 Not Found", "<h1>404 Not Found</h1>")

    except Exception as e:
        print(f"Error handling request: {e}")
        return generate_response("500 Internal Server Error", "<h1>500 Internal Server Error</h1>")

# Log HTTP requests
def log_request(method, path):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {method} {path}")

# Handle email sending via SMTP
def handle_send_email(path):
    query = parse_qs(urlparse(path).query)
    recipient = query.get('to', [None])[0]
    subject = query.get('subject', [None])[0]
    message = query.get('message', [None])[0]

    if not (recipient and subject and message):
        return generate_response("400 Bad Request", "<h1>400 Bad Request</h1><p>Missing email parameters.</p>")

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(EMAIL_ADDRESS, recipient, email_message)

        return generate_response("200 OK", f"<h1>Email Sent</h1><p>Email successfully sent to {recipient}.</p>")
    except Exception as e:
        print(f"SMTP Error: {e}")
        return generate_response("500 Internal Server Error", "<h1>500 Internal Server Error</h1><p>Could not send email.</p>")

# Handle client connections
def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        if not request:
            return
        response = handle_request(request)
        client_socket.sendall(response.encode())
    finally:
        client_socket.close()

# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server running on http://{HOST}:{PORT}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address}")
            Thread(target=handle_client, args=(client_socket,)).start()
    except KeyboardInterrupt:
        print("\nShutting down the server")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
