#!/usr/bin/env python3
"""
Simple Python HTTP server that returns "hello"
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

class HelloHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler that returns hello"""
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'hello')
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'healthy')
            
        elif self.path == '/ready':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'ready')
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        # Simple logging
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def main():
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, HelloHandler)
    print(f"Starting hello server on http://0.0.0.0:8080")
    print("Endpoints:")
    print("  GET /       -> hello")
    print("  GET /health -> health check")
    print("  GET /ready  -> readiness check")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down hello server...")
        httpd.shutdown()

if __name__ == "__main__":
    main()
