from Resources import Resources
from UserInfo import UserInfo
from Colors import Colors
import Utility
import Data
import State

class Player():
    def __init__(self, connection):
        self.connection = connection
        self.loggedIn = False
        self.state = State.INIT
    
    def InitUserInfo(self):
        self.info = UserInfo()
        Data.users_info.append((self.username, self.info))
    
    def LoadUserInfo(self):
        for username_arg, info_arg in Data.users_info:
            if username_arg == self.username:
                self.info = info_arg
        
    def InitResources(self):
        self.resources = Resources()
        self.resources.Init(7000, 250, 250, 30)
        Data.resources.append((self.username, self.resources))
        
    def LoadResources(self):
        for username_arg, resources_arg in Data.resources:
            if username_arg == self.username:
                self.resources = resources_arg
    
    def ShowResources(self):        
        Utility.SendMsg(self, Colors.COLOR_GREEN + "Resources:\n")
        for resType, resAmount in self.resources.iteritems():
            Utility.SendMsg(self, resType.color + resType.name + " = " + str(resAmount) + "\n")
        
        Utility.SendMsg(self, Colors.COLOR_GREEN + "UserInfo:\n") 
        Utility.SendMsg(self, Colors.COLOR_GOLD + "buildingsBuildToday: " + str(self.info.buildingsBuildToday) + "\n")
        Utility.SendMsg(self, Colors.COLOR_BROWN + "unitsRecruitedToday: " + str(self.info.unitsRecruitedToday) + "\n")
        Utility.SendMsg(self, Colors.COLOR_STEEL + "maxNumberOfUnits: " + str(self.info.maxNumberOfUnits) + "\n")
        Utility.SendMsg(self, Colors.COLOR_VIOLET + "numberOfUnits: " + str(self.info.numberOfUnits) + "\n")   
        
    def Pay(self, cost, percent):
        for resType, resAmount in cost.iteritems():
            pAmount = int(resAmount * percent/100.0)
            resDiff = pAmount - self.resources[resType]
            if resDiff > 0:
                Utility.SendMsg(self, Colors.COLOR_RED + "You need " + str(resDiff) + " more " + resType.name + "!\n" )
                return False
        for resType, resAmount in cost.iteritems():
            pAmount = int(resAmount * percent/100.0)
            self.resources[resType] -= pAmount
        return True
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        