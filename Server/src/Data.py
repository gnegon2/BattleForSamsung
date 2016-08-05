import threading

class Data():
    def Init(self):
        self.users = []
        self.resources = []
        self.users_info = []
        
    def Load(self, obj):
        self.map = obj.map
        self.users = obj.users
        self.resources = obj.resources
        self.users_info = obj.users_info

mainData = Data()
dbLock = threading.Lock()