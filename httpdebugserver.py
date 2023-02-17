#!/usr/bin/python3

import http.server
import socketserver
import sys
import time

DEFAULT_PORT=8000


class ServerHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, content_length=0):
        self.send_response(200)
        self.send_header('Connection', 'close')
        self.send_header('Content-type', 'application/json')
        if content_length > 0:
            self.send_header('Content-Length', content_length)
        self.end_headers()
    
    def do_HEAD(self):
        # print(f"HEAD {self.path}")
        self._set_headers()

    def do_GET(self):
        # print(f"GET {self.path}")
        self._set_headers()
        with open(self.path.lstrip('/'), 'rb') as f:
            self.wfile.write(f.read())

    def do_POST(self):
        # print(f"POST {self.path}")
        with open(self.path.lstrip('/'), 'rb') as f:
            data = f.read()
        self.close_connection = False
        self._set_headers(len(data))
        self.wfile.write(data)
        self.wfile.flush()
        time.sleep(0.1)


def main():
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    Handler = ServerHandler

    with http.server.HTTPServer(("", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()


if __name__ == "__main__":
    main()