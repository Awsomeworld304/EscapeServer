import datetime
import os

class FakeDB:
    LOG_LEVEL = "ERROR"
    db_path = './db.dat'

    event_name:str = "No Event"
    event_type:str = "No Event"
    event_status:str = "Inactive"

    rooms = "No Rooms"

    start_date:str = "No Event"
    end_date:str = "No Event"

    event_types:dict = {
        'Fire': '',
        'Shooting': '',
        'Weather': '',
        'Flood': ''
        }
    
    def __init__(self, LOG_LVL:str="ERROR")->None:
        self.LOG_LEVEL = LOG_LVL
        last_line = ""
        with open(self.db_path, 'rb') as f:
            try:  # catch OSError in case of a one line file 
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            self.last_line = f.readline().decode()
        """
        if ":" in last_line: 
            data = last_line.split(":")[1].split(",")
            self.event_name = data[0]
            self.event_type = data[1]
            self.event_status = data[2]
            self.start_date = data[3]
            self.end_date = data[4]
            self.rooms = data[5]
        """
        self.update_logs(True)
        pass
    
    def update_logs(self, init:bool=False)->None:
        log_file_handle = open(self.db_path, "a")
        if init == True: log_file_handle.write("---SESSION START---\n"); return
        line = str(datetime.datetime.now()) + ":" + self.event_name + "," + self.event_type + "," + self.event_status + "," + self.start_date + "," + self.end_date + "," + self.rooms + "\n"
        log_file_handle.write(line)
        log_file_handle.close()
        if self.LOG_LEVEL == "INFO": print("DB: Written to log: " + line)
        pass
    
    def on_exit(self):
        log_file_handle = open(self.db_path, "a")
        log_file_handle.write("---SESSION END---\n")
        log_file_handle.close()
        pass

    def get_tags()->str: return "event_name,event_type,event_status,start_date,end_date,rooms"
    def get_name(self)->str: return self.event_name
    def get_type(self)->str: return self.event_type
    def get_status(self)->str: return self.event_status
    def get_start_date(self)->str: return self.start_date
    def get_end_date(self)->str: return self.end_date
    def get_rooms(self)->str: return self.rooms
    def get_all(self)->str: return self.event_name + "," + self.event_type + "," + self.event_status + "," + self.start_date + "," + self.end_date + "," + self.rooms
    def get_from_tag(self,tag)->str:
        match tag:
            case "event_name": return self.get_name()
            case "event_type": return self.get_type()
            case "event_status": return self.get_status()
            case "start_date": return self.get_start_date()
            case "end_date": return self.get_end_date()
            case "rooms": return self.get_rooms()
            case _: return "Unknown tag."

    def set_name(self, event_name:str)->bool: 
        self.event_name = event_name
        self.update_logs()
        return True
    def set_type(self, event_type:str)->bool: 
        self.event_type = event_type
        self.update_logs()
        return True
    def set_status(self, event_status:str)->bool: 
        self.event_status = event_status
        self.update_logs()
        return True
    def set_start_date(self, start_date:str=datetime.datetime.now())->bool: 
        self.start_date = start_date
        self.update_logs()
        return True
    def set_end_date(self, end_date:str=datetime.datetime.now())->bool: 
        self.end_date = end_date
        self.update_logs()
        return True
    def set_rooms(self, rooms:str="")->bool: 
        self.rooms = rooms
        self.update_logs()
        return True
    def set_from_tag(self,tag,value)->str:
        match tag:
            case "event_name": self.set_name(value)
            case "event_type": self.set_type(value)
            case "event_status": self.set_status(value)
            case "start_date": self.set_start_date(value)
            case "end_date": self.set_end_date(value)
            case "rooms": self.set_rooms(value)
            case _: return "Unknown tag."
        return "Value written successfully."
    
    def add_event_type(self, type:str, msg:str):
        self.event_types.update({type: msg})
        pass
    def del_event_type(self, type:str):
        del self.event_types[type]
        pass
    
    def reset(self)->None:
        self.event_name = "No Event"
        self.event_type = "No Event"
        self.event_status = "Inactive"
        self.start_date = "No Event"
        self.end_date = "No Event"
        self.rooms = "No Rooms"
        print("DB: The event has been reset.")
        self.update_logs()
        pass
    pass