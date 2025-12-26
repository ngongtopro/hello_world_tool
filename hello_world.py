#!/usr/bin/env python3
"""
Hello World Tool - HTTP Server
A simple tool that prints "Hello World" message via HTTP
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
from datetime import datetime
from urllib.parse import urlparse, parse_qs

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "localhost"

def run_hello_world(name=None):
    """Run the Hello World function"""
    message = "=" * 50 + "\n"
    message += "        HELLO WORLD TOOL\n"
    message += "=" * 50 + "\n"
    
    if name:
        message += f"\n🌟 Hello, {name}! 🌟\n\n"
        message += f"Welcome {name} to your first tool!\n"
    else:
        message += "\n🌟 Hello, World! 🌟\n\n"
        message += "Welcome to your first tool!\n"
    
    message += "=" * 50
    return message

class HelloWorldHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Hello World"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path.startswith('/hello') or self.path.startswith('/?'):
            # Parse URL and get query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Get 'name' parameter if provided
            name = query_params.get('name', [None])[0]
            if name:
                name = name.strip()
            
            # Run Hello World with name
            message = run_hello_world(name)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Print to console
            if name:
                print(f"\n[{timestamp}] Request received from {self.client_address[0]} with name: {name}")
            else:
                print(f"\n[{timestamp}] Request received from {self.client_address[0]}")
            print(message)
            
            # Send HTTP response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            response = f"[{timestamp}]\n{message}\n"
            self.wfile.write(response.encode('utf-8'))
        else:
            # 404 for other paths
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        pass  # We handle logging in do_GET

def main():
    """Main function to start the HTTP server"""
    PORT = 5010
    HOST = '0.0.0.0'  # Listen on all network interfaces
    
    server = HTTPServer((HOST, PORT), HelloWorldHandler)
    local_ip = get_local_ip()
    
    print("=" * 60)
    print("        HELLO WORLD TOOL - HTTP SERVER")
    print("=" * 60)
    print(f"\n🚀 Server is running!")
    print(f"\n📍 Access URLs:")
    print(f"   - Local:   http://localhost:{PORT}")
    print(f"   - Network: http://{local_ip}:{PORT}")
    print(f"\n💡 Other devices on the same network can access:")
    print(f"   http://{local_ip}:{PORT}")
    print(f"\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        server.shutdown()

if __name__ == "__main__":
    main()
