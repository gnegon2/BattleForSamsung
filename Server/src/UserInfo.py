import time;

class UserInfo():
    def __init__(self):
        self.registeredDate = time.localtime(time.time())
        self.LastGathered = time.localtime(time.time())
        self.LastBuild = time.localtime(time.time())
        self.LastRecruit = time.localtime(time.time())
        self.buildingsBuildToday = 0
        self.unitsRecruitedToday = 0
        self.maxNumberOfUnits = 0
        self.numberOfUnits = 0