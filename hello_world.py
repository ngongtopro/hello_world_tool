#!/usr/bin/env python3
"""
Hello World Tool - REST API Server
A multi-endpoint REST API tool with various functionalities
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import json
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

def get_server_info():
    """Get server information"""
    return {
        "server": "Hello World Tool API",
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/",
            "/hello",
            "/info",
            "/status",
            "/time",
            "/echo",
            "/greet"
        ]
    }

def get_status():
    """Get server status"""
    return {
        "status": "running",
        "uptime": "active",
        "healthy": True,
        "timestamp": datetime.now().isoformat()
    }

def get_time():
    """Get current server time"""
    now = datetime.now()
    return {
        "datetime": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "timezone": "Local",
        "unix_timestamp": int(now.timestamp())
    }

class HelloWorldHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Hello World API"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Route: / or /hello - Hello World
        if path == '/' or path == '/hello':
            name = query_params.get('name', [None])[0]
            if name:
                name = name.strip()
            
            message = run_hello_world(name)
            
            # Log to console
            if name:
                print(f"\n[{timestamp}] GET {path} - Request from {self.client_address[0]} with name: {name}")
            else:
                print(f"\n[{timestamp}] GET {path} - Request from {self.client_address[0]}")
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            response = f"[{timestamp}]\n{message}\n"
            self.wfile.write(response.encode('utf-8'))
        
        # Route: /info - Server information
        elif path == '/info':
            print(f"\n[{timestamp}] GET /info - Request from {self.client_address[0]}")
            
            info = get_server_info()
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(info, indent=2).encode('utf-8'))
        
        # Route: /status - Server status
        elif path == '/status':
            print(f"\n[{timestamp}] GET /status - Request from {self.client_address[0]}")
            
            status = get_status()
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(status, indent=2).encode('utf-8'))
        
        # Route: /time - Current time
        elif path == '/time':
            print(f"\n[{timestamp}] GET /time - Request from {self.client_address[0]}")
            
            time_info = get_time()
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(time_info, indent=2).encode('utf-8'))
        
        # Route: /echo - Echo query parameters
        elif path == '/echo':
            print(f"\n[{timestamp}] GET /echo - Request from {self.client_address[0]}")
            
            message = query_params.get('message', [''])[0]
            response_data = {
                "echo": message if message else "No message provided",
                "received_at": timestamp,
                "client_ip": self.client_address[0],
                "all_params": {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
        
        # Route: /greet - Greeting with language support
        elif path == '/greet':
            name = query_params.get('name', ['World'])[0]
            lang = query_params.get('lang', ['en'])[0].lower()
            
            greetings = {
                'en': f'Hello, {name}!',
                'vi': f'Xin chào, {name}!',
                'es': f'¡Hola, {name}!',
                'fr': f'Bonjour, {name}!',
                'de': f'Hallo, {name}!',
                'ja': f'こんにちは, {name}!',
                'ko': f'안녕하세요, {name}!',
                'zh': f'你好, {name}!'
            }
            
            greeting = greetings.get(lang, greetings['en'])
            
            print(f"\n[{timestamp}] GET /greet - Request from {self.client_address[0]} - {lang}: {name}")
            
            response_data = {
                "greeting": greeting,
                "name": name,
                "language": lang,
                "timestamp": timestamp,
                "available_languages": list(greetings.keys())
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, indent=2, ensure_ascii=False).encode('utf-8'))
        
        else:
            # 404 for unknown paths
            print(f"\n[{timestamp}] GET {path} - 404 Not Found - Request from {self.client_address[0]}")
            
            error_data = {
                "error": "Not Found",
                "message": f"The endpoint '{path}' does not exist",
                "available_endpoints": get_server_info()["endpoints"],
                "timestamp": timestamp
            }
            
            self.send_response(404)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(error_data, indent=2).encode('utf-8'))
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ''
        
        # Route: /echo - Echo POST data
        if path == '/echo':
            print(f"\n[{timestamp}] POST /echo - Request from {self.client_address[0]}")
            
            try:
                # Try to parse as JSON
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                data = {"raw_body": body}
            
            response_data = {
                "method": "POST",
                "received_data": data,
                "timestamp": timestamp,
                "client_ip": self.client_address[0]
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
        
        else:
            # Method not allowed for this path
            print(f"\n[{timestamp}] POST {path} - 405 Method Not Allowed - Request from {self.client_address[0]}")
            
            error_data = {
                "error": "Method Not Allowed",
                "message": f"POST is not supported for '{path}'",
                "supported_methods": ["GET"],
                "timestamp": timestamp
            }
            
            self.send_response(405)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(error_data, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        pass  # We handle logging in do_GET and do_POST

def main():
    """Main function to start the HTTP server"""
    PORT = 5010
    HOST = '0.0.0.0'  # Listen on all network interfaces
    
    server = HTTPServer((HOST, PORT), HelloWorldHandler)
    local_ip = get_local_ip()
    
    print("=" * 60)
    print("        HELLO WORLD TOOL - REST API SERVER")
    print("=" * 60)
    print(f"\n🚀 Server is running!")
    print(f"\n📍 Access URLs:")
    print(f"   - Local:   http://localhost:{PORT}")
    print(f"   - Network: http://{local_ip}:{PORT}")
    print(f"\n📚 Available API Endpoints:")
    print(f"   GET  /              - Hello World")
    print(f"   GET  /hello?name=X  - Hello with name")
    print(f"   GET  /info          - Server information")
    print(f"   GET  /status        - Server status")
    print(f"   GET  /time          - Current time")
    print(f"   GET  /echo?msg=X    - Echo message")
    print(f"   GET  /greet?name=X&lang=vi - Multi-language greeting")
    print(f"   POST /echo          - Echo JSON data")
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
