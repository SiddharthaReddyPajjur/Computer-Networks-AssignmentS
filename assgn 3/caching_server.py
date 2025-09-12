import http.server
import socketserver
import os
import hashlib
from datetime import datetime
from email.utils import formatdate

PORT = 8000
HTML_FILE = 'index.html'

class CachingRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get file stats: modification time and content
            file_path = HTML_FILE
            file_stat = os.stat(file_path)
            with open(file_path, 'rb') as f:
                file_content = f.read()

            # --- Create server's cache validators ---
            # 1. Last-Modified header based on file's modification time 
            last_modified_time = file_stat.st_mtime
            last_modified_str = formatdate(timeval=last_modified_time, localtime=False, usegmt=True)

            # 2. ETag header based on the MD5 hash of the file content 
            file_hash = hashlib.md5(file_content).hexdigest()
            etag = f'"{file_hash}"'

            # --- Check client's headers ---
            client_etag = self.headers.get('If-None-Match')
            client_modified_since = self.headers.get('If-Modified-Since')

            # Check if client's cache is still valid 
            if client_etag == etag or client_modified_since == last_modified_str:
                # If it is, tell them they have the latest version 
                self.send_response(304) # 304 Not Modified
                self.end_headers()
                print(f"'{HTML_FILE}' is already cached by the client. Sent 304 Not Modified.")
                return

            # --- If cache is invalid, send the file ---
            # Send a 200 OK response with the file and new cache headers 
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(file_content))
            self.send_header('Last-Modified', last_modified_str)
            self.send_header('ETag', etag)
            self.end_headers()
            self.wfile.write(file_content)
            print(f"Sent '{HTML_FILE}' with new ETag and Last-Modified headers.")

        except FileNotFoundError:
            self.send_error(404, 'File Not Found: %s' % self.path)

# Start the server
with socketserver.TCPServer(("", PORT), CachingRequestHandler) as httpd:
    print(f"Serving at port {PORT}. Open http://localhost:{PORT} in your browser.")
    print("Modify index.html and refresh the page to see caching in action.")
    httpd.serve_forever()
