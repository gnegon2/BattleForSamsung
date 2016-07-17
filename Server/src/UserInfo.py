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
        self.LastGathered = time.localtime(time.time())
        self.LastBuild = time.localtime(time.time())
        self.LastRecruit = time.localtime(time.time())
        self.buildingsBuildToday = 0
        self.unitsRecruitedToday = 0
        self.maxNumberOfUnits = 0
        self.numberOfUnits = 0
        self.color = random.sample(colors,  1)[0]
        colors.remove(self.color)