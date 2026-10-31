"""
EvidenceBot - Landing Page Server
=================================
Serves the modern, responsive EvidenceBot landing page on port 5173.
"""

import http.server
import socketserver
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PORT = 5173
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'landing')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Concise logging
        sys.stdout.write(f"[Landing Server] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()

def main():
    socketserver.TCPServer.allow_reuse_address = True
    print(f"Starting Landing Page server on port {PORT}...")
    print(f"Directory: {DIRECTORY}")
    sys.stdout.flush()
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"SUCCESS: Landing Page is LIVE at http://localhost:{PORT}")
            sys.stdout.flush()
            httpd.serve_forever()
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
