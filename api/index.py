from http.server import BaseHTTPRequestHandler
import subprocess
import sys
import os

# Start Streamlit process on initial cold start
cmd = [
    sys.executable,
    "-m",
    "streamlit",
    "run",
    "app.py",
    "--server.port=8080",
    "--server.address=0.0.0.0",
    "--server.headless=true"
]
subprocess.Popen(cmd)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Streamlit server starting up...")
        return