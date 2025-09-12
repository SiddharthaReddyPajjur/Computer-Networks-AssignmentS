import socket

HOST, PORT = '', 8080

def create_http_response(body, headers_extra=""):
    """A helper function to create a full HTTP response string."""
    response_body = f"<html><body><h1>{body}</h1></body></html>"
    content_length = len(response_body)
    response_headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {content_length}\r\n"
        f"{headers_extra}"
        "\r\n" # An empty line to separate headers from the body
    )
    return response_headers + response_body

# Create a TCP socket
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print(f'Serving HTTP on port {PORT}...')

while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024).decode('utf-8')
    print(f"Received request:\n---\n{request_data.strip()}\n---")

    # Check if the request has a 'Cookie' header 
    if 'Cookie: user_id=User123' in request_data:
        # If cookie exists, welcome the user back 
        print("Cookie found! This is a returning visitor.")
        http_response = create_http_response("Welcome back, User123!")
    else:
        # If no cookie, it's a new visitor. Give them one. [cite: 26]
        print("No cookie found. This is a new visitor.")
        # The 'Set-Cookie' header tells the browser to store this cookie [cite: 28]
        set_cookie_header = "Set-Cookie: user_id=User123\r\n"
        http_response = create_http_response(
            "Welcome, new friend! I've given you a cookie.",
            headers_extra=set_cookie_header
        )

    # Send the response and close the connection
    client_connection.sendall(http_response.encode())
    client_connection.close()
