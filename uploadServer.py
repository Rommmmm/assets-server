#!/bin/python3

from http.server import BaseHTTPRequestHandler,HTTPServer
import cgi

ADDR = ""
PORT = 6969

class RequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
                if self.path == "/upload":
                        length = int(self.headers['content-length'])
                        print ("Receiving file %s bytes " % (length))
                        form = cgi.FieldStorage(
                                fp=self.rfile,
                                headers=self.headers,
                                environ={'REQUEST_METHOD':'POST',
                                        'CONTENT_TYPE':self.headers['Content-Type'],
                                        })      
                        filename = form['file'].filename
                        data = form['file'].file.read()
                        open("/tmp/%s"%filename, "wb").write(data)
                        print("uploaded %s"%filename)
                        self.send_response(200)
                        self.send_header("Content-type", self.headers['Content-Type'].encode())
                        self.end_headers()
                else:
                        self.send_response(404)
try:
        httpd = HTTPServer((ADDR, PORT), RequestHandler)
        httpd.serve_forever()

except KeyboardInterrupt:
        print (" received, shutting down the web server")
        httpd.socket.close()
