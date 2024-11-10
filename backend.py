import  sys,os
import http.server
import requests
import socket
import json
#from tinydb import TinyDB, Query
from urllib.parse import urlparse
import sqlite3
from sqlite3 import Error

import FakeDB

#import BufferedDB

"""
A lot more work is needed to make the web panel!
However the API and DB is the main point of the server, not a web UI. 
"""

db_token = ""
with open('./assets/master.key', 'r') as f: db_token = f.read()

# Local IP obv, we are NOT about to have this on the web!!
ip = socket.gethostbyname(socket.gethostname())

# Clear prev logs...
os.system("cls")

# Simple DB
#db = BufferedDB.BufferedDB()
#db = TinyDB('db.json')
db = FakeDB.FakeDB()

def minimenu()->bool:
    ye = input("Would you like to host the website? (y/N): ")
    if ye.lower == "y": return True
    return False

hostSite = minimenu()

class Server(http.server.BaseHTTPRequestHandler):
    file_to_open = ""

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', self.content_type)
        #self.send_header('Content-Length', self.path.getsize(self.getPath()))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        pass

    def do_GET(self):
        if self.path == '/':
            if hostSite:
                self.path = './static/index.html'
                try: file_to_open = open(self.path).read(); self.send_response(200)
                except: file_to_open = "File not found!"; self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes(file_to_open, 'utf-8'))
            else:
                file_to_open = "Server is active!\nHowever, the dashboard is disabled."
                self.end_headers()
                self.send_response(200)
                self.wfile.write(bytes(file_to_open, 'utf-8'))
        # Other file loading
        elif os.path.isfile(f'.{self.path}'):
            try: file_to_open = open(f'.{self.path}').read(); self.send_response(200)
            except: file_to_open = "File not found!"; self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
            pass

        #* GET API STUFF
        elif self.path == '/api/get/test':
            file_to_open = "Test!"
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b'Test of the server API.')
            pass
        # Gets list of whole DB.
        elif self.path == '/getall':
            file_to_open = db.get_all()
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
            pass

        # /getvalue?tag=test
        elif self.path.__contains__("/getvalue?tag="):
            q = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in q.split("&"))
            tag = query_components["tag"]
            print(f"tag: {tag}")
            file_to_open = db.get_from_tag(tag)
            #db.get(tag) if db.get(tag) != None else "null"
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
            pass

        # /setvalue?tag=test&value=test
        elif self.path.__contains__("/setvalue?tag=") and self.path.__contains__("&value="):
            q = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in q.split("&"))
            tag = query_components["tag"]
            val = query_components["value"]
            print(f"tag: {tag} value: {val}")
            file_to_open = db.set_from_tag(tag,val)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
            pass
        
        #* Whatever else!!!
        else:
            file_to_open = "Unknown call: " + self.path
            print(file_to_open)
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
            pass
        
        """ Server Web Panel Stuff (Broken)
        elif self.path == '/api/data':
            self._set_headers('application/json')
            response = {'message': 'Hello from Python HTTP Server!'}
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            pass
        """
        pass
    
    def do_POST(self):
        if self.path == "/api/post/test":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            print("Received POST data:", post_data)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"POST request processed: " + post_data)
            pass
        pass

def init():
    #print(f'DB Server at http://{ip}:8081')
    print(f'Web Server at: http://{ip}:8080')
    httpd = http.server.ThreadingHTTPServer((ip,8080),Server)
    httpd.serve_forever()
    pass

init()