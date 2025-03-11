import socket
import argparse
from urllib.parse import urlparse, urlencode

def send_post_request(url, params):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    path = parsed_url.path if parsed_url.path else "/"
    port = parsed_url.port if parsed_url.port else 80
    
    post_data = urlencode(params)
    request = (f"POST {path} HTTP/1.1\r\n"
               f"Host: {host}\r\n"
               f"Content-Type: application/x-www-form-urlencoded\r\n"
               f"Content-Length: {len(post_data)}\r\n"
               f"Connection: close\r\n\r\n"
               f"{post_data}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())
        response = s.recv(4096)
    
    print(response.decode(errors='ignore'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a POST request via raw socket")
    parser.add_argument("--url", required=True, help="Target URL")
    known_args, unknown_args = parser.parse_known_args()
    
    params = {}
    it = iter(unknown_args)
    for arg in it:
        if arg.startswith("--"):
            key = arg[2:]
            value = next(it, "")
            params[key] = value
    
    send_post_request(known_args.url, params)