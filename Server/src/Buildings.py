from Resources import Resources
from Commands import BuildingCommands
from LocalMapStruct import localMaps
import Utility
import Control
from Statistics import Statistics

def CommandToBuilding(command):
    if command == BuildingCommands.BANK:
        return Bank
    elif command == BuildingCommands.HOUSE:
        return House
    elif command == BuildingCommands.SAW_MILL:
        return SawMill
    elif command == BuildingCommands.LIBRARY:
        return Library
    elif command == BuildingCommands.MINE:
        return Mine
    elif command == BuildingCommands.CRYSTAL_MINE:
        return CrystalMine
    elif command == BuildingCommands.WALL:
        return Wall
    elif command == BuildingCommands.TOWER:
        return Tower
    else:
        return Empty
    
def Build(player, building):
    for resType, resAmount in building.cost.iteritems():
        resDiff = resAmount - player.resources[resType]
        if resDiff > 0:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You need " + str(resDiff) + " more " + resType.name + "!\n" )
            return False
    for resType, resAmount in building.cost.iteritems():
        player.resources[resType] -= resAmount
    return True

def ShowInfo(player, building):
    Utility.SendMsg(player, Control.CTRL_COLOR_AZURE + building.__name__ + ": \n")
    Utility.SendMsg(player, building.ExtraInfo())
    Utility.SendMsg(player, Control.CTRL_COLOR_ORANGE + "Cost: \n")
    for iType, iAmount in building.cost.iteritems():
        if iAmount > 0:
            Utility.SendMsg(player, iType.color + iType.name + ": " + str(iAmount) + "\n")
    
    if hasattr(building, 'production'):
        Utility.SendMsg(player, Control.CTRL_COLOR_ORANGE + "Production: \n")
        for iType, iAmount in building.production.iteritems():
            if iAmount > 0:
                Utility.SendMsg(player, iType.color + iType.name + ": " + str(iAmount) + "\n")
    
    Utility.SendMsg(player, Control.CTRL_COLOR_ORANGE + "Statistics: \n")
    for iType, iAmount in building.statistics.iteritems():
        if iAmount > 0:
            Utility.SendMsg(player, iType.color + iType.name + ": " + str(iAmount) + "\n")    
    
def GetProduction(player, building):
    if hasattr(building, 'production'):
        Utility.SendMsg(player, Control.CTRL_COLOR_AZURE + building.__class__.__name__ + " produce: \n")
        for iType, iAmount in building.production.iteritems():
            if iAmount > 0:
                Utility.SendMsg(player, iType.color + iType.name + ": " + str(iAmount) + "\n")
                player.resources[iType] += iAmount

class Building(object):
    
    def __new__(typ, *args, **kwargs):
        obj = object.__new__(typ, *args, **kwargs)
        obj.owner = args[0]
        return obj

class Empty():
    def __init__(self):
        self.field = "0"
        self.color = Control.CTRL_COLOR_BROWN
        
class Forbidden():
    def __init__(self):
        self.field = "X"
        self.color = Control.CTRL_COLOR_POPPY

class Fortress(Building):
    field = "F"
    color = Control.CTRL_COLOR_POPPY
        
    cost = Resources()
    cost.Init(200, 5, 5, 1)
    
    production = Resources()
    production.Init(20, 1, 1)
    
    statistics = Statistics()
    statistics.Init(1000, 100, 10, 5, 10, 1)
    
    army_production = 1
    
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
        self.production = self.__class__.production
        
        self.army_production = self.__class__.army_production
        self.owner.info.maxNumberOfUnits += self.army_production
        print "self.owner.info.maxNumberOfUnits=" + str(self.owner.info.maxNumberOfUnits)
        
    def __del__(self):
        self.owner.info.maxNumberOfUnits -= self.army_production
        print "del self.owner.info.maxNumberOfUnits=" + str(self.owner.info.maxNumberOfUnits)
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Control.CTRL_COLOR_GREEN
        extraInfoMsg += "Fortress is the main building on the map.\n"
        extraInfoMsg += "It provides resources and army production.\n"
        return extraInfoMsg
    
class Bank(Building):
    field = "B" 
    color = Control.CTRL_COLOR_GOLD
    
    cost = Resources()
    cost.Init(40, 5, 5)
    
    production = Resources()
    production.Init(60)
    
    statistics = Statistics()
    statistics.Init(100, 20)
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
        self.production = self.__class__.production
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Control.CTRL_COLOR_GREEN
        extraInfoMsg += "Each bank provide you a lot of money.\n"
        return extraInfoMsg
    
class House(Building):
    field = "H"
    color = Control.CTRL_COLOR_GREEN
    
    cost = Resources()
    cost.Init(50, 4, 2)
    
    statistics = Statistics()
    statistics.Init(250, 30)
      
    army_production = 5
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
        
        self.army_production = self.__class__.army_production
        self.owner.info.maxNumberOfUnits += self.army_production
        print "self.owner.info.maxNumberOfUnits=" + str(self.owner.info.maxNumberOfUnits)
    
    def __del__(self):
        self.owner.info.maxNumberOfUnits -= self.army_production   
        print "del self.owner.info.maxNumberOfUnits=" + str(self.owner.info.maxNumberOfUnits)
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Control.CTRL_COLOR_GREEN
        extraInfoMsg += "Each house provide you to recruit more army.\n"
        return extraInfoMsg

class SawMill(Building):
    field = "S"
    color = Control.CTRL_COLOR_WOOD
    
    cost = Resources()
    cost.Init(40, 5)
    
    production = Resources()
    production.Init(0, 5)
    
    statistics = Statistics()
    statistics.Init(200, 25)
    
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
        self.production = self.__class__.production
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Control.CTRL_COLOR_GREEN
        extraInfoMsg += "Saw mill provide you a lot of wood.\n"
        return extraInfoMsg
    
class Library(Building):
    field = "L"
    color = Control.CTRL_COLOR_AZURE
    
    cost = Resources()
    cost.Init(150, 4, 4, 1)
    
    statistics = Statistics()
    statistics.Init(50, 10)  
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
        
        localMaps[self.owner.localMapY][self.owner.localMapX].librariesCount += 1
        print "librariesCount=" + str(localMaps[self.owner.localMapY][self.owner.localMapX].librariesCount)
        
    def __del__(self):
        localMaps[self.owner.localMapY][self.owner.localMapX].librariesCount -= 1  
        print "librariesCount=" + str(localMaps[self.owner.localMapY][self.owner.localMapX].librariesCount)
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Control.CTRL_COLOR_GREEN
        extraInfoMsg += "Each library give you access to a new unit.\n"
        return extraInfoMsg
    
class Mine(Building):
    field = "M"
    color = Control.CTRL_COLOR_STEEL
    
    cost = Resources()
    cost.Init(60, 4)
    
    production = Resources()
    production.Init(0, 0, 5)
    
    statistics = Statistics()
    statistics.Init(100, 20)  
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
        self.production = self.__class__.production
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Control.CTRL_COLOR_GREEN
        extraInfoMsg += "Mine provide you a lot of stone.\n"
        return extraInfoMsg
    
class CrystalMine(Building):
    field = "C"
    color = Control.CTRL_COLOR_VIOLET
    
    cost = Resources()
    cost.Init(200, 4, 4)
    
    production = Resources()
    production.Init(0, 0, 0, 1)
    
    statistics = Statistics()
    statistics.Init(150, 30) 
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
        self.production = self.__class__.production
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Control.CTRL_COLOR_GREEN
        extraInfoMsg += "Crystal mine provide you a crystals.\n"
        return extraInfoMsg
    
class Wall(Building):
    field = "W"
    color = Control.CTRL_COLOR_GRANAT
    
    cost = Resources()
    cost.Init(40, 1, 1)
    
    statistics = Statistics()
    statistics.Init(500, 50) 
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Control.CTRL_COLOR_GREEN
        extraInfoMsg += "Wall defends your fortress.\n"
        return extraInfoMsg
    
class Tower(Building):
    field = "T"
    color = Control.CTRL_COLOR_BLOOD
    
    cost = Resources()
    cost.Init(120, 3, 3)
    
    statistics = Statistics()
    statistics.Init(700, 60, 20, 10, 20, 3) 
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Control.CTRL_COLOR_GREEN
        extraInfoMsg += "Tower attack nearby enemy and defends your fortress.\n"
        return extraInfoMsg