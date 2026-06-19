#!/usr/bin/env python3
"""Simple HTTP server exposing the current directory on 0.0.0.0:5000.

Run with:
    python server.py

The server will serve files from the directory where the script is located.
"""
import http.server
import socketserver

HOST = "0.0.0.0"
PORT = 5000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
    print(f"Serving HTTP on {HOST} port {PORT} (http://{HOST}:{PORT}/) ...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()
