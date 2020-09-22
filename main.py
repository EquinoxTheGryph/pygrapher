from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from datetime import datetime as time

import grapher

file_path = "data.json"
output_path = "out.png"
port = 8080


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Please use a POST request containing the history JSON to recieve a plot!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        
        with open(file_path, "wb") as file:
            file.write(body)
        
        grapher.graph(file_path, output_path)
        
        with open(output_path, "rb") as file:
            self.wfile.write(file.read())
        
        print(time.now().time(), "-> Success at ip:", self.client_address[0])


httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
print("Server started!")
httpd.serve_forever()
