from Commands import UnitsCommands
import Control
import Utility
from Resources import Resources
from Statistics import Statistics

def CommandToUnit(player, command):
    if command == UnitsCommands.PEASANT:
        return Peasant
    elif command == UnitsCommands.ARCHER:
        return Archer
    elif command == UnitsCommands.SWORDMAN:
        return Swordman
    elif command == UnitsCommands.PIKEMAN:
        return Pikeman
    elif command == UnitsCommands.CROSSBOWMAN:
        return Crossbowman
    elif command == UnitsCommands.HORSEMAN:
        return Horseman
    elif command == UnitsCommands.CATAPULT:
        return Catapult
    elif command == UnitsCommands.CANNON:
        return Cannon
    else:
        return Empty

def Buy(player, unit):
    for resType, resAmount in unit.cost.iteritems():
        resDiff = resAmount - player.resources[resType]
        if resDiff > 0:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You need " + str(resDiff) + " more " + resType.name + "!\n" )
            return False
    for resType, resAmount in unit.cost.iteritems():
        player.resources[resType] -= resAmount
    return True
    
def ShowInfo(player, unit):
    Utility.SendMsg(player, Control.CTRL_COLOR_AZURE + unit.__class__.__name__ + ": \n")
    Utility.SendMsg(player, unit.ExtraInfo())
    Utility.SendMsg(player, Control.CTRL_COLOR_ORANGE + "Cost: \n")
    for iType, iAmount in unit.cost.iteritems():
        if iAmount > 0:
            Utility.SendMsg(player, iType.color + iType.name + ": " + str(iAmount) + "\n")
        
    Utility.SendMsg(player, Control.CTRL_COLOR_ORANGE + "Statistics: \n")
    for iType, iAmount in unit.statistics.iteritems():
        if iAmount > 0:
            Utility.SendMsg(player, iType.color + iType.name + ": " + str(iAmount) + "\n") 

class Empty():
    'Empty Unit'

class Unit(object): 
    
    def __new__(typ, *args, **kwargs):
        obj = object.__new__(typ, *args, **kwargs)
        obj.owner = args[0]
        obj.movedInTurn = False
        obj.attackedInTurn = False
        obj.owner.info.numberOfUnits += 1
        print "obj.owner.info.numberOfUnits=" + str(obj.owner.info.numberOfUnits)
        return obj
    
    def __del__(self):
        self.owner.info.numberOfUnits -= 1
        print "del obj.owner.info.numberOfUnits=" + str(self.owner.info.numberOfUnits)
        
class Peasant(Unit):
    cost = Resources()
    cost.Init(5)
    statistics = Statistics()
    statistics.Init(10, 2, 1, 1, 2, 1, 1)
    
    def __init__(self, player):
        self.field = "1"
        self.color = Control.CTRL_COLOR_GREEN
        self.statistics = self.__class__.statistics
        
    @staticmethod
    def ExtraInfo():
        return "Peasant is the stupid man with fork.\n"

class Archer(Unit):
    cost = Resources()
    cost.Init(20)
    statistics = Statistics()
    statistics.Init(20, 3, 2, 2, 4, 3, 1)
        
    def __init__(self, player):
        self.field = "2"
        self.color = Control.CTRL_COLOR_GOLD
        self.statistics = self.__class__.statistics
    
    @staticmethod
    def ExtraInfo():
        return "Archer can attack on distance.\n"
    
class Swordman(Unit):
    cost = Resources()
    cost.Init(50, 0, 1)
    statistics = Statistics()
    statistics.Init(50, 8, 6, 5, 8, 1, 1)
    
    def __init__(self, player):
        self.field = "3"
        self.color = Control.CTRL_COLOR_STEEL
        self.statistics = self.__class__.statistics
    
    @staticmethod
    def ExtraInfo():
        return "Swordman is a strong unit in armor.\n"
    
class Pikeman(Unit):
    cost = Resources()
    cost.Init(70, 1)
    statistics = Statistics()
    statistics.Init(70, 10, 7, 6, 12, 2, 2)
    
    def __init__(self, player):
        self.field = "4" 
        self.color = Control.CTRL_COLOR_GRANAT
        self.statistics = self.__class__.statistics     
    
    @staticmethod
    def ExtraInfo():
        return "Pikeman is best against horseman.\n"
     
class Crossbowman(Unit):
    cost = Resources()
    cost.Init(80, 1, 1)
    statistics = Statistics()
    statistics.Init(70, 8, 8, 10, 12, 4, 2)
                    
    def __init__(self, player):
        self.field = "5" 
        self.color = Control.CTRL_COLOR_ORANGE
        self.statistics = self.__class__.statistics
        
    @staticmethod
    def ExtraInfo():
        return "Crossbowman is a very strong range unit.\n"
    
class Horseman(Unit):
    cost = Resources()
    cost.Init(100, 2)
    statistics = Statistics()
    statistics.Init(100, 15, 10, 12, 15, 1, 4)
                    
    def __init__(self, player):
        self.field = "6" 
        self.color = Control.CTRL_COLOR_WOOD
        self.statistics = self.__class__.statistics
    
    @staticmethod
    def ExtraInfo():
        return "Horseman is a very fast unit.\n"
    
class Catapult(Unit):
    cost = Resources()
    cost.Init(150, 2, 2)
    statistics = Statistics()
    statistics.Init(150, 12, 15, 15, 20, 6, 1)
    
    def __init__(self, player):
        self.field = "7" 
        self.color = Control.CTRL_COLOR_BLOOD
        self.statistics = self.__class__.statistics
        
    @staticmethod
    def ExtraInfo():
        return "Catapult can attack at very high distance.\n"
    
class Cannon(Unit):
    cost = Resources()
    cost.Init(200, 2, 2, 1)
    statistics = Statistics()
    statistics.Init(200, 20, 20, 20, 20, 4, 2)
                    
    def __init__(self, player):
        self.field = "8" 
        self.color = Control.CTRL_COLOR_AZURE
        self.statistics = self.__class__.statistics
        
    @staticmethod
    def ExtraInfo():
        return "Cannon is the most powerfull unit.\n"
