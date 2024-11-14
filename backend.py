import  sys,os
import http.server
import requests
import socket
import json
from urllib.parse import urlparse

import FakeDB

"""
A lot more work is needed to make the web panel!
However the API and DB is the main point of the server, not a web UI. 
"""
# The location of the server log, not to be confused with the database location.
SERVER_LOG = "./server.log"

# Can be "INFO", "ERROR", "NONE". 
# "ERROR" only includes anything else other than '200' responses.
LOG_LEVEL = "ERROR"

db_token = ""
with open('./assets/master.key', 'r') as f: db_token = f.read()

# Local IP obv, we are NOT about to have this on the web!!
ip = socket.gethostbyname(socket.gethostname())

# Clear prev logs...
os.system("cls")

# Simple DB
db = FakeDB.FakeDB()
awing = ["1A - CTE Math", "1AA - Direct Care Worker", "2A - Option Pathway", "3A - Success Lab", "4A - Practical Nursing", "5A - Practical Nursing", "6A - Pre-Engineering / PLTW", "7A - HVAC", "8A - Electrical", "9A - Certified Patient Care Technician", "10A - Dental Assisting/Clinic", "11A - Masonry", "A Wing Hallway"]
bwing = ["1B - Cafeteria", "2B - ProStart", "3B - ProStart", "3BB - Masonry", "4B - Misc.", "4BB - SkillsUSA", "5B - Carpentry", "6B - Welding", "8B - Carpentry Shop", "9B - Automotive", "10B - Welding Shop", "11B - Collision Repair", "12B - Collision Repair Shop", "13B - Cybersecurity", "14B - CTE English", "B Wing Hallway"]
cwing = ["1C - Option Pathway", "2C - Law and Public Safety", "3C - Plumbing", "4C - Diesel Technology", "4CC - Diesel Technology Shop", "5C - Emergency and Firefighting Management Services", "6C - Graphic Design / Multimedia Publishing", "7C - Medical Assisting", "C Wing Hallway"]
other = ["Lobby", "Office", "Commons"]

# Client ID List (ID is a four digit unique number.)
ids:list = []
latest_id:int = 0000

def check_id(self, id)->bool:
    for i in ids: 
        if i == id: return False
    ids.append(id)
    return True

def minimenu()->bool:
    ye = input("Would you like to host the website? (y/N): ")
    if ye.lower == "y": return True
    return False

hostSite:bool = True

class Server(http.server.BaseHTTPRequestHandler):
    file_to_open:str = ""

    def _set_headers(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        #self.send_header('Content-Length', self.path.getsize(self.getPath()))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        pass

        
    def log_message(self, format, *args):
        msg = "%s - - [%s] %s\n" %(self.address_string(),self.log_date_time_string(),format%args)
        match LOG_LEVEL:
            case "INFO": open(SERVER_LOG, "a").write(msg) 
            case "ERROR":
                if not msg.__contains__("200"): open(SERVER_LOG, "a").write(msg); print(msg)
            case "NONE": return
        pass
        

    def do_OPTIONS(self):
        self._set_headers()

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
        elif self.path == '/api/events':
            self._set_headers('application/json')
            response = {
                    'event_name': db.get_name(),
                    'event_type': db.get_type(),
                    'event_status': db.get_status(),
                    'start_date': db.get_start_date(),
                    'end_date': db.get_end_date(),
                    'rooms': db.get_rooms()
                }
            #response = {'message': 'No events found'}
            self.wfile.write(json.dumps(response).encode())
        # Checks for new update.
        elif self.path == "/new?id=":
            q = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in q.split("&"))
            id = query_components["id"]
            check_id(id)

            file_to_open = ""
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
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
            file_to_open = db.get_from_tag(tag)
            print(f"tag: {tag}, value: {file_to_open}")
            if file_to_open == "Unknown tag.":
                file_to_open = "Invalid tag!"
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(bytes(file_to_open, 'utf-8'))
            else:
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
        
        # Make a whole event with just query string LOL
        elif self.path.__contains__("/setvalue?event_name=") and self.path.__contains__("&event_type=") and self.path.__contains__("&event_status=") and self.path.__contains__("&start_date=")  and self.path.__contains__("&end_date=") and self.path.__contains__("&rooms="):
            q = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in q.split("&"))
            print("Event Creation Request has been received.")
            db.set_from_tag("event_name", query_components["event_name"])
            db.set_from_tag("event_type", query_components["event_type"])
            db.set_from_tag("event_status", query_components["event_status"])
            db.set_from_tag("start_date", query_components["start_date"])
            db.set_from_tag("end_date", query_components["end_date"])
            db.set_from_tag("rooms", query_components["rooms"])
            file_to_open = "Event created successfully."
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
            pass
        
        #* Unknown Route
        else:
            file_to_open = "Unknown call: " + self.path
            print(file_to_open)
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
            pass
        pass
    
    # Mainly for the web panel although it can be used anywhere else.
    def do_POST(self):
        if self.path == '/api/events':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            event_data = json.loads(post_data)
            if event_data["event_name"] != "": db.set_from_tag("event_name", event_data["event_name"])
            if event_data["event_type"] != "": db.set_from_tag("event_type", event_data["event_type"])
            if event_data["event_status"] != "": db.set_from_tag("event_status", event_data["event_status"])
            if event_data["start_date"] != "": db.set_from_tag("start_date", event_data["start_date"])
            if event_data["end_date"] != "": db.set_from_tag("end_date", event_data["end_date"])
            if event_data["rooms"] != "": db.set_from_tag("rooms", event_data["rooms"])
            print("Web Event gotten from Browser")
            #print(db.get_all())
            self._set_headers('application/json')
            response = {'message': 'Event created successfully!'}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint not found!")
        pass

def init():
    print(f'Web Server at: http://{ip}:8080')
    httpd = http.server.ThreadingHTTPServer((ip,8080),Server)
    httpd.serve_forever()
    pass

init()