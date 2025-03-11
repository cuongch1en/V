import socket
import ssl
import argparse
import os
from urllib.parse import urlparse

def download_via_socket(url):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    path = parsed_url.path if parsed_url.path else '/'
    port = 443 if parsed_url.scheme == 'https' else 80
    
    # Tạo socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Nếu là HTTPS, sử dụng SSL
        if parsed_url.scheme == 'https':
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)
        
        # Gửi HTTP GET request
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        sock.sendall(request.encode())
        
        # Nhận dữ liệu từ socket
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
        
        sock.close()
        
        # Phân tích phản hồi HTTP
        header, _, body = response.partition(b"\r\n\r\n")
        
        # Xác định tên file từ URL
        filename = os.path.basename(path) if os.path.basename(path) else "index.html"
        
        # Lưu nội dung vào file
        with open(filename, "wb") as f:
            f.write(body)
        
        print(f"Downloaded and saved as {filename}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a file using socket (supports HTTP and HTTPS)")
    parser.add_argument("--url", required=True, help="URL to download")
    args = parser.parse_args()
    
    download_via_socket(args.url)