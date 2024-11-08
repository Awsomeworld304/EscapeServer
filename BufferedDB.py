from sqlite3 import Error
import sqlite3
from collections import deque
from enum import Enum
#from typing import List

class BufferedDB:

    db = None
    path = ""

    class EventType(Enum):
        FIRE = "Fire"
        TORNADO = "Tornado"
        SHOOTING = "School Shooting"
        FLOOD = "Flash Flood"
        GAS = "Gas Leak"
        OTHER = "Unknown Event: Check Logs"
    
    class EventStatus(Enum):
        ACTIVE = "Active Event"
        INACTIVE = "Inactive Event"

    create_events_table:str = open("./sql/create_events_table.sql").read()
    print(create_events_table)

    def create_connection(self)->None:
        connection = None
        try: connection = sqlite3.connect(self.path); print("DB: Connection to SQLite DB successful.")
        except Error as e: print(f"DB: Error connecting to database: {e}")
        return connection


    def __init__(self, db_path="./sql/db.sqlite")->None:
        print("DB: Init...")
        self.path = db_path
        self.db = self.create_connection()
        obj = self.db.cursor()
        obj.executescript(str(self.create_events_table))
        obj.close()
        #self.db.execute(self.db, self.create_events_table)
        pass

    def add_event(self, event_name:str, event_type:EventType, rooms:list, status:EventStatus)->None:
        '''
        Event Name - Name of the event.\n
        Event Type (EventType) - The type of event.\n
        Rooms (Rooms List) - The list of affected rooms.\n
        Status (EventStatus) - The current status of the event.
        '''
        insert = f"INSERT INTO events (event_name,event_type,rooms,status) VALUES ({event_name}, {event_type}, {rooms}, {status})"
        obj = self.db.cursor()
        obj.executescript(insert)
        obj.close()
        #self.db.executes(self.db, insert)
        print("DB: Event added: " + obj)
        pass

    def get_event(self)->None:
        pass

    def get(self, tag)->str:
        val:str = tag
        print(f"DB: Val = {val}")
        return val