import socket
import re

HOST = '127.0.0.1'
PORT = 3000

target = r"GET\s+(/[^\s]*)"


def get_content_type(path: str) -> str:
    
    if re.match(r'.*(html)', path):
        return "text/html"
    if re.match(r'.*(css)', path):
        return "text/css"
    if re.match(r'.*(js)', path):
        return "application/javascript"
    return "text/plain"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Listening at http://localhost:3000")

    while True:
        new_socket, addr = s.accept()
        new_socket.settimeout(1)
        print("New socket:", new_socket)
        print("Address:", addr)

        request = new_socket.recv(1024)
        print("Request:",request)

        path = re.match(target, request.decode())
        if path:
            path = path.group(1)
        else:
            path = "/"

        if path == "/":
            path = "/index.html"

        path = "./site" + path

        try:
            f = open(path, 'rb')
            body = f.read()
            status = "HTTP/1.1 200 OK"
            content_type = get_content_type(path) 
        except:
            f = None
            body = b"<h1>404 Not Found<h1>"
            status = "HTTP/1.1 404 Not Found"
            content_type = "text/html"

        response = status + "\r\n" + "Content-Type: " + content_type + "\r\n" + "Content-Length: " + str(len(body)) + "\r\n" + "Connection: close\r\n\r\n"

        response = response.encode() + body
        new_socket.sendall(response)
        new_socket.close() 

        
