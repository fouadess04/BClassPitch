#!/usr/bin/env python3
"""Simple HTTP server exposing the current directory on 0.0.0.0:5000.

Run with:
    python server.py

The server will serve files from the directory where the script is located.
"""
import http.server
import socketserver
import os
import sys
import time
import threading
import importlib

HOST = "0.0.0.0"
PORT = 5000

def watch_index_file():
    html_path = 'index.html'
    last_mtime = None
    if os.path.exists(html_path):
        last_mtime = os.path.getmtime(html_path)
        
    # Ensure current directory is in sys.path
    if '' not in sys.path:
        sys.path.insert(0, '')
    import update_eff

    while True:
        try:
            if os.path.exists(html_path):
                current_mtime = os.path.getmtime(html_path)
                if last_mtime is None or current_mtime != last_mtime:
                    last_mtime = current_mtime
                    importlib.reload(update_eff)
                    update_eff.run_update_if_needed()
        except Exception as e:
            print(f"Error in file watcher: {e}")
        time.sleep(2)

# Start background file watcher thread
watcher_thread = threading.Thread(target=watch_index_file, daemon=True)
watcher_thread.start()

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
    print(f"Serving HTTP on {HOST} port {PORT} (http://{HOST}:{PORT}/) ...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()
