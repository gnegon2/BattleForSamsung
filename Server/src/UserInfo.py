import time;
import random
from Colors import Colors

colors = []
for key, value in vars(Colors).iteritems():
    if not (key.startswith('__')) and isinstance(value, basestring):
        colors.append(value)

class UserInfo():
    def __init__(self):
        self.registeredDate = time.localtime(time.time())
        self.LastBuild = time.localtime(time.time())
        self.LastRecruit = time.localtime(time.time())
        self.buildingsBuildToday = 0
        self.unitsRecruitedToday = 0
        self.maxNumberOfUnits = 0
        self.numberOfUnits = 0
        self.color = random.sample(colors,  1)[0]
        colors.remove(self.color)
        
    def CheckLastBuild(self):
        actualTime = time.localtime(time.time())
        if self.LastBuild.tm_year < actualTime.tm_year or \
            self.LastBuild.tm_mon < actualTime.tm_mon or \
            self.LastBuild.tm_mday < actualTime.tm_mday or \
            self.LastBuild.tm_hour + 5 < actualTime.tm_hour:
            self.LastBuild = actualTime
            self.buildingsBuildToday = 0
    
    def CheckLastRecruit(self):
        actualTime = time.localtime(time.time())
        if self.LastRecruit.tm_year < actualTime.tm_year or \
            self.LastRecruit.tm_mon < actualTime.tm_mon or \
            self.LastRecruit.tm_mday < actualTime.tm_mday or \
            self.LastRecruit.tm_hour + 5 < actualTime.tm_hour:
            self.LastRecruit = actualTime
            self.unitsRecruitedToday = 0