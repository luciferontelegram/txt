"""
Simple HTTP server for Koyeb/Heroku that keeps the app alive
Run this alongside main.py if you need a web server
"""

import os
import http.server
import socketserver
from threading import Thread
import subprocess
import sys

# Get port from environment, default to 8080
PORT = int(os.environ.get('PORT', 8080))

# Simple HTTP request handler
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Advance TXT Uploader Bot is running!')
    
    def log_message(self, format, *args):
        # Suppress log messages
        return

def run_server():
    """Run a simple HTTP server to keep the app alive"""
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

def run_bot():
    """Run the main bot process"""
    subprocess.run([sys.executable, "main.py"])

if __name__ == "__main__":
    # Start the HTTP server in a thread
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Run the bot in the main thread
    print("Starting bot...")
    run_bot()
