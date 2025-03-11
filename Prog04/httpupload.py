import socket
import argparse
import os
import mimetypes
from urllib.parse import urlparse

def send_file(url, user, password, file_path):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    path = parsed_url.path if parsed_url.path else "/"
    port = parsed_url.port if parsed_url.port else 80
    
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    filename = os.path.basename(file_path)
    content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    
    with open(file_path, "rb") as f:
        file_content = f.read()
    
    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"user\"\r\n\r\n{user}\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"password\"\r\n\r\n{password}\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\n"
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode() + file_content + f"\r\n--{boundary}--\r\n".encode()
    
    headers = (
        f"POST {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n\r\n"
    ).encode()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(headers + body)
        response = s.recv(4096)
    
    print(response.decode(errors='ignore'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload file via raw socket")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--user", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")
    parser.add_argument("--local-file", required=True, help="Path to the local file")
    args = parser.parse_args()
    
    send_file(args.url, args.user, args.password, args.local_file)