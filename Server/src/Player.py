from Resources import Resources
from Control import Control
from Utility import Utility
from Data import Data
from UserInfo import UserInfo
from State import State

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
        self.resources.Add(Resources.GOLD, 2500)
        self.resources.Add(Resources.WOOD, 100)
        self.resources.Add(Resources.STONE, 100)
        self.resources.Add(Resources.CRYSTALS, 50)
        
        Data.resources.append((self.username, self.resources))
        
    def LoadResources(self):
        for username_arg, resources_arg in Data.resources:
            if username_arg == self.username:
                self.resources = resources_arg
    
    def ShowResources(self):
        Utility.SendMsg(self, Control.CTRL_COLOR_GREEN + "Resources:\n")
        Utility.SendMsg(self, Control.CTRL_COLOR_GOLD + "Gold: " + str(self.resources.gold) + "\n")
        Utility.SendMsg(self, Control.CTRL_COLOR_BROWN + "Wood: " + str(self.resources.wood) + "\n")
        Utility.SendMsg(self, Control.CTRL_COLOR_STEEL + "Stone: " + str(self.resources.stone) + "\n")
        Utility.SendMsg(self, Control.CTRL_COLOR_VIOLET + "Crystals: " + str(self.resources.crystals) + "\n")       
        