import datetime

class FakeDB:
    event_name:str = ""
    event_type:str = ""
    event_status:str = ""

    start_date:str = ""
    end_date:str = ""
    
    def __init__(self)->None:
        pass
    
    def update_logs(self)->None:
        log_file_handle = open("./db-log.dat", "a")
        line = datetime.datetime.now() + ":" + self.event_name + "," + self.event_type + "," + self.event_status + "," + self.start_date + "," + self.end_date
        log_file_handle.write(line)
        print("DB: Written to log.")
        pass

    def get_name(self)->str: return self.event_name
    def get_type(self)->str: return self.event_type
    def get_status(self)->str: return self.event_status
    def get_start_date(self)->str: return self.start_date
    def get_end_date(self)->str: return self.end_date
    def get_all(self)->str: return self.event_name + "," + self.event_type + "," + self.event_status + "," + self.start_date + "," + self.end_date

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
        self.event_status = start_date
        self.update_logs()
        return True
    def set_end_date(self, end_date:str=datetime.datetime.now())->bool: 
        self.event_status = end_date
        self.update_logs()
        return True
    
    def reset(self)->None:
        self.event_name = ""
        self.event_type = ""
        self.event_status = ""
        self.start_date = ""
        self.end_date = ""
        print("DB: The event has been reset.")
        self.update_logs()
        pass
    pass