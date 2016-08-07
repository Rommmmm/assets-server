#!/bin/python3

from http.server import BaseHTTPRequestHandler,HTTPServer
import cgi
import time

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
                        timestamp = str(time.time())
                        filename = form['file'].filename
                        fullname = timestamp + filename
                        data = form['file'].file.read()
                        open("/tmp/%s"%fullname, "wb").write(data)
                        print("uploaded %s"%fullname)
                        self.send_response(200)
                        self.send_header("Content-type", self.headers['Content-Type'].encode())
                        self.end_headers()
                        self.wfile.write(bytes("File: %s successfully uploaded\n" % filename, 'utf-8'))
                        self.wfile.write(bytes("Path on server is : /tmp/%s" %fullname, 'utf-8'))
                else:
                        self.send_response(404)
                        self.wfile.write(bytes("TEST", 'utf-8'))
try:    
        print ("Server is running on port:", PORT)
        httpd = HTTPServer((ADDR, PORT), RequestHandler)
        httpd.serve_forever()

except KeyboardInterrupt:
        print (" received, shutting down the web server")
        httpd.socket.close()

