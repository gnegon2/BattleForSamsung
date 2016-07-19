from Resources import Resources
from Commands import BuildingCommands
from Colors import Colors
from Statistics import Statistics
from copy import copy
import Utility
import Map

def CommandToBuilding(command):
    if command == BuildingCommands._0_0_HOUSE:
        return House
    elif command == BuildingCommands._1_0_BANK:
        return Bank
    elif command == BuildingCommands._2_0_SAW_MILL:
        return SawMill
    elif command == BuildingCommands._3_0_MINE:
        return Mine
    elif command == BuildingCommands._4_0_CRYSTAL_MINE:
        return CrystalMine
    elif command == BuildingCommands._5_0_WALL:
        return Wall
    elif command == BuildingCommands._6_0_TOWER:
        return Tower
    elif command == BuildingCommands._7_0_LIBRARY:
        return Library
    else:
        return Empty;
    
def ShowInfo(player, building):
    Utility.SendMsg(player, Colors.COLOR_AZURE + building.__name__ + ": \n")
    Utility.SendMsg(player, building.ExtraInfo())
    Utility.SendMsg(player, Colors.COLOR_ORANGE + "Cost: \n")
    for iType, iAmount in building.cost.iteritems():
        if iAmount > 0:
            Utility.SendMsg(player, iType.color + iType.name + ": " + str(iAmount) + "\n")
    
    if hasattr(building, 'production'):
        Utility.SendMsg(player, Colors.COLOR_ORANGE + "Production: \n")
        for iType, iAmount in building.production.iteritems():
            if iAmount > 0:
                Utility.SendMsg(player, iType.color + iType.name + ": " + str(iAmount) + "\n")
    
    Utility.SendMsg(player, Colors.COLOR_ORANGE + "Statistics: \n")
    for iType, iAmount in building.statistics.iteritems():
        if iAmount > 0:
            Utility.SendMsg(player, iType.color + iType.name + ": " + str(iAmount) + "\n")    
    
def GetProduction(resource, building):
    if hasattr(building, 'production'):
        for iType, iAmount in building.production.iteritems():
            if iAmount > 0:
                resource[iType] += iAmount
    return resource

class Building(object):
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        obj.owner = args[0]
        return obj

class Empty():
    field = "0"
    color = Colors.COLOR_BROWN
    
    def __init__(self):
        self.field = self.__class__.field
        self.color = self.__class__.color
        
class Forbidden():
    def __init__(self):
        self.field = "X"
        self.color = Colors.COLOR_POPPY

class Fortress(Building):
    field = "F"
    color = Colors.COLOR_POPPY
        
    cost = Resources()
    cost.Init(200, 5, 5, 1)
    
    production = Resources()
    production.Init(20, 1, 1)
    
    statistics = Statistics()
    statistics.Init(250, 10, 3, 3, 5, 6)
    
    army_production = 1
    
    def __init__(self, player):
        self.level = 1
        
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = copy(self.__class__.statistics)
        self.production = self.__class__.production
        
        self.army_production = self.__class__.army_production
        self.owner.info.maxNumberOfUnits += self.army_production
        print "self.owner.info.maxNumberOfUnits=" + str(self.owner.info.maxNumberOfUnits)
        
    def __del__(self):
        self.owner.info.maxNumberOfUnits -= self.army_production
        print "del self.owner.info.maxNumberOfUnits=" + str(self.owner.info.maxNumberOfUnits)
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Fortress is the main building on the map.\n"
        extraInfoMsg += "It provides resources and army production.\n"
        return extraInfoMsg

class House(Building):
    field = "H"
    color = Colors.COLOR_GREEN
    
    cost = Resources()
    cost.Init(50, 4, 2)
    
    statistics = Statistics()
    statistics.Init(120, 4)
      
    army_production = 5
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = copy(self.__class__.statistics)
        
        self.army_production = self.__class__.army_production
        self.owner.info.maxNumberOfUnits += self.army_production
        print "self.owner.info.maxNumberOfUnits=" + str(self.owner.info.maxNumberOfUnits)
    
    def __del__(self):
        self.owner.info.maxNumberOfUnits -= self.army_production   
        print "del self.owner.info.maxNumberOfUnits=" + str(self.owner.info.maxNumberOfUnits)
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Each house provide you to recruit more army.\n"
        return extraInfoMsg

class Bank(Building):
    field = "B" 
    color = Colors.COLOR_GOLD
    
    cost = Resources()
    cost.Init(40, 5, 5)
    
    production = Resources()
    production.Init(60)
    
    statistics = Statistics()
    statistics.Init(80, 4)
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = copy(self.__class__.statistics)
        self.production = self.__class__.production
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Each bank provide you a lot of money.\n"
        return extraInfoMsg

class SawMill(Building):
    field = "S"
    color = Colors.COLOR_WOOD
    
    cost = Resources()
    cost.Init(40, 5)
    
    production = Resources()
    production.Init(0, 5)
    
    statistics = Statistics()
    statistics.Init(80, 4)
    
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = copy(self.__class__.statistics)
        self.production = self.__class__.production
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Saw mill provide you a lot of wood.\n"
        return extraInfoMsg
    
class Mine(Building):
    field = "M"
    color = Colors.COLOR_STEEL
    
    cost = Resources()
    cost.Init(60, 4)
    
    production = Resources()
    production.Init(0, 0, 5)
    
    statistics = Statistics()
    statistics.Init(100, 5)  
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = copy(self.__class__.statistics)
        self.production = self.__class__.production
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Mine provide you a lot of stone.\n"
        return extraInfoMsg
    
class CrystalMine(Building):
    field = "C"
    color = Colors.COLOR_VIOLET
    
    cost = Resources()
    cost.Init(200, 4, 4)
    
    production = Resources()
    production.Init(0, 0, 0, 1)
    
    statistics = Statistics()
    statistics.Init(120, 5) 
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = copy(self.__class__.statistics)
        self.production = self.__class__.production
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Crystal mine provide you a crystals.\n"
        return extraInfoMsg
    
class Wall(Building):
    field = "W"
    color = Colors.COLOR_AZURE
    
    cost = Resources()
    cost.Init(40, 1, 1)
    
    statistics = Statistics()
    statistics.Init(100, 10) 
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = copy(self.__class__.statistics)
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Wall defends your fortress.\n"
        return extraInfoMsg
    
class Tower(Building):
    field = "T"
    color = Colors.COLOR_BLOOD
    
    cost = Resources()
    cost.Init(250, 3, 3, 1)
    
    statistics = Statistics()
    statistics.Init(150, 8, 6, 8, 10, 6) 
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = copy(self.__class__.statistics)
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Tower attack nearby enemy and defends your fortress.\n"
        return extraInfoMsg
    
class Library(Building):
    field = "L"
    color = Colors.COLOR_AZURE
    
    cost = Resources()
    cost.Init(150, 4, 4, 1)
    
    statistics = Statistics()
    statistics.Init(50, 4)  
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = copy(self.__class__.statistics)
        
        Map.ChangeFortLevel(self.owner.wy, self.owner.wx, 1)
        
    def __del__(self):
        Map.ChangeFortLevel(self.owner.wy, self.owner.wx, -1)
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Each library give you access to a new unit.\n"
        return extraInfoMsg