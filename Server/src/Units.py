from Commands import UnitsCommands
from Colors import Colors
from Resources import Resources
from Statistics import Statistics
from copy import copy
import Utility
import inspect

def CommandToUnit(command):
    if command == UnitsCommands._1_0_PEASANT:
        return Peasant
    elif command == UnitsCommands._2_0_ARCHER:
        return Archer
    elif command == UnitsCommands._3_0_SWORDMAN:
        return Swordman
    elif command == UnitsCommands._4_0_PIKEMAN:
        return Pikeman
    elif command == UnitsCommands._5_0_CROSSBOWMAN:
        return Crossbowman
    elif command == UnitsCommands._6_0_HORSEMAN:
        return Horseman
    elif command == UnitsCommands._7_0_CATAPULT:
        return Catapult
    elif command == UnitsCommands._8_0_CANNON:
        return Cannon
    else:
        return Empty
    
def ShowInfo(player, unit):
    if inspect.isclass(unit):
        Utility.SendMsg(player, Colors.COLOR_AZURE + unit.__name__ + ": \n")
        Utility.SendMsg(player, unit.ExtraInfo())
    Utility.SendMsg(player, Colors.COLOR_ORANGE + "Cost: \n")
    for iType, iAmount in unit.cost.iteritems():
        if iAmount > 0:
            Utility.SendMsg(player, iType.color + iType.name + ": " + str(iAmount) + "\n")
        
    Utility.SendMsg(player, Colors.COLOR_ORANGE + "Statistics: \n")
    for iType, iAmount in unit.statistics.iteritems():
        if iAmount > 0:
            Utility.SendMsg(player, iType.color + iType.name + ": " + str(iAmount) + "\n") 

class Empty():
    'Empty Unit'

class Unit(object): 
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        obj.owner = args[0]
        obj.owner.info.numberOfUnits += 1
        print "obj.owner.info.numberOfUnits=" + str(obj.owner.info.numberOfUnits)
        return obj
    
    def __del__(self):
        self.owner.info.numberOfUnits -= 1
        print "del obj.owner.info.numberOfUnits=" + str(self.owner.info.numberOfUnits)
        
class Peasant(Unit):
    field = "1"
    cost = Resources()
    cost.Init(5)
    statistics = Statistics()
    statistics.Init(15, 3, 2, 2, 4, 1, 1)
    
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = Colors.COLOR_GREEN
        self.statistics = copy(self.__class__.statistics)
        
    @staticmethod
    def ExtraInfo():
        return Colors.COLOR_GREEN + "Peasant is the stupid man with fork.\n"

class Archer(Unit):
    field = "2"
    cost = Resources()
    cost.Init(20)
    statistics = Statistics()
    statistics.Init(20, 3, 3, 3, 4, 3, 1)
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = Colors.COLOR_GOLD
        self.statistics = copy(self.__class__.statistics)
    
    @staticmethod
    def ExtraInfo():
        return Colors.COLOR_GREEN +"Archer can attack on distance.\n"
    
class Swordman(Unit):
    field = "3"
    cost = Resources()
    cost.Init(50, 0, 1)
    statistics = Statistics()
    statistics.Init(40, 6, 5, 5, 8, 1, 1)
    
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = Colors.COLOR_STEEL
        self.statistics = copy(self.__class__.statistics)
    
    @staticmethod
    def ExtraInfo():
        return Colors.COLOR_GREEN + "Swordman is a strong unit in armor.\n"
    
class Pikeman(Unit):
    field = "4"
    cost = Resources()
    cost.Init(70, 1)
    statistics = Statistics()
    statistics.Init(60, 8, 7, 6, 8, 2, 2)
    
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = Colors.COLOR_AZURE
        self.statistics = copy(self.__class__.statistics)     
    
    @staticmethod
    def ExtraInfo():
        return Colors.COLOR_GREEN + "Pikeman is best against horseman.\n"
     
class Crossbowman(Unit):
    field = "5"
    cost = Resources()
    cost.Init(80, 1, 1)
    statistics = Statistics()
    statistics.Init(60, 8, 8, 10, 12, 4, 2)
                    
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = Colors.COLOR_ORANGE
        self.statistics = copy(self.__class__.statistics)
        
    @staticmethod
    def ExtraInfo():
        return Colors.COLOR_GREEN + "Crossbowman is a very strong range unit.\n"
    
class Horseman(Unit):
    field = "6"
    cost = Resources()
    cost.Init(100, 2)
    statistics = Statistics()
    statistics.Init(80, 12, 10, 12, 15, 1, 4)
                    
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = Colors.COLOR_WOOD
        self.statistics = copy(self.__class__.statistics)
    
    @staticmethod
    def ExtraInfo():
        return Colors.COLOR_GREEN + "Horseman is a very fast unit.\n"
    
class Catapult(Unit):
    field = "7"
    cost = Resources()
    cost.Init(150, 2, 2)
    statistics = Statistics()
    statistics.Init(100, 10, 15, 15, 20, 6, 1)
    
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = Colors.COLOR_BLOOD
        self.statistics = copy(self.__class__.statistics)
        
    @staticmethod
    def ExtraInfo():
        return Colors.COLOR_GREEN + "Catapult can attack at very high distance.\n"
    
class Cannon(Unit):
    field = "8"
    cost = Resources()
    cost.Init(200, 2, 2, 1)
    statistics = Statistics()
    statistics.Init(200, 20, 20, 20, 20, 4, 2)
                    
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = Colors.COLOR_AZURE
        self.statistics = copy(self.__class__.statistics)
        
    @staticmethod
    def ExtraInfo():
        return Colors.COLOR_GREEN + "Cannon is the most powerfull unit.\n"
