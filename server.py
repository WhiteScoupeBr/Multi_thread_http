from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import socket
import threading
import codecs
import os
import sys

#Get the IP
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

print("Connect to:", get_ip())


#print (local_ip)
HOST = get_ip()

PORT = 3000

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

class handler (BaseHTTPRequestHandler): 

    def do_GET(self):
        print(self.headers)
        print(threading.currentThread().getName())
        self.handle_request()

    def do_POST(self):
        content_length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_length)
        self.write_response(body)
        print(threading.currentThread().getName())
        self.handle_request()
        
    def write_response(self, content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content)

        print(self.headers)
        print(content.decode('utf-8'))    


    def handle_request(self):
        message = ''
        if('index/' in self.path):
            request1 = self.path.split("index/",1)[1] 
            print("request:",request1)
            self.send_response(200)
            message = codecs.open("index.html", 'r')
        elif('index' in self.path):
            self.send_response(200)
            message = codecs.open("index.html")

        else:
            self.send_response(404)
            message = codecs.open("erro.html", 'r')
        
        self.send_header('Connection', 'close')
        self.end_headers()

        self.wfile.write(message.read().encode('utf8'))

    def send_response(self, code, message=None):
        self.send_response_only(code, message)
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())

def main():
    httpServer = ThreadingSimpleServer((HOST, PORT), handler)

    try:
        httpServer.serve_forever()
    except KeyboardInterrupt:
        pass
    httpServer.server_close()
    print("Closing connection")

if __name__ == '__main__':
    main()