from Resources import Resources
from Commands import BuildingCommands
from Colors import Colors
from Statistics import Statistics
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
        return Empty
    
def Pay(player, building):
    for resType, resAmount in building.cost.iteritems():
        resDiff = resAmount - player.resources[resType]
        if resDiff > 0:
            Utility.SendMsg(player, Colors.COLOR_RED + "You need " + str(resDiff) + " more " + resType.name + "!\n" )
            return False
    for resType, resAmount in building.cost.iteritems():
        player.resources[resType] -= resAmount
    return True

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
    
def GetProduction(player, building):
    if hasattr(building, 'production'):
        Utility.SendMsg(player, Colors.COLOR_AZURE + building.__class__.__name__ + " produce: \n")
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
    production.Init(80, 4, 4)
    
    statistics = Statistics()
    statistics.Init(1000, 10, 10, 5, 10, 1)
    
    army_production = 1
    
    def __init__(self, player):
        self.level = 1
        
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
    statistics.Init(100, 20)
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
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
    statistics.Init(200, 25)
    
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
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
    statistics.Init(100, 20)  
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
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
    statistics.Init(150, 30) 
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
        self.production = self.__class__.production
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Crystal mine provide you a crystals.\n"
        return extraInfoMsg
    
class Wall(Building):
    field = "W"
    color = Colors.COLOR_GRANAT
    
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
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Wall defends your fortress.\n"
        return extraInfoMsg
    
class Tower(Building):
    field = "T"
    color = Colors.COLOR_BLOOD
    
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
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Tower attack nearby enemy and defends your fortress.\n"
        return extraInfoMsg
    
class Library(Building):
    field = "L"
    color = Colors.COLOR_AZURE
    
    cost = Resources()
    cost.Init(150, 4, 4, 1)
    
    statistics = Statistics()
    statistics.Init(50, 10)  
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = self.__class__.statistics
        
        fortress = Map.GetFort(self.owner.wy, self.owner.wx)
        fortress.level += 1
        print "librariesCount=" + str(fortress.level)
        
    def __del__(self):
        fortress = Map.GetFort(self.owner.wy, self.owner.wx)
        fortress.level -= 1
        print "librariesCount=" + str(fortress.level)
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Each library give you access to a new unit.\n"
        return extraInfoMsg