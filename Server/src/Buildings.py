from Resources import Resources
from Commands import BuildingCommands
from Colors import Colors
from Statistics import Statistics
from copy import copy
import Utility
import time
import inspect

def InitFortressLevels():
    # Level 1
    level_cost_1 = Resources()
    level_cost_1.Init(500, 10, 10, 2)
    Fortress.cost_per_level.append(level_cost_1)
    level_production_1 = Resources()
    level_production_1.Init(20, 1, 1)
    Fortress.production_per_level.append(level_production_1)
    level_statistics_1 = Statistics()
    level_statistics_1.Init(250, 10, 3, 3, 5, 6)
    Fortress.statistics_per_level.append(level_statistics_1)
    # Level 2
    level_cost_2 = Resources()
    level_cost_2.Init(200, 5, 5, 0, 2)
    Fortress.cost_per_level.append(level_cost_2)
    level_production_2 = Resources()
    level_production_2.Init(30, 1, 1)
    Fortress.production_per_level.append(level_production_2)
    level_statistics_2 = Statistics()
    level_statistics_2.Init(350, 12, 4, 3, 5, 6)
    Fortress.statistics_per_level.append(level_statistics_2)
    # Level 3
    level_cost_3 = Resources()
    level_cost_3.Init(400, 7, 7, 0, 4)
    Fortress.cost_per_level.append(level_cost_3)
    level_production_3 = Resources()
    level_production_3.Init(40, 1, 1)
    Fortress.production_per_level.append(level_production_3)
    level_statistics_3 = Statistics()
    level_statistics_3.Init(500, 15, 5, 4, 5, 6)
    Fortress.statistics_per_level.append(level_statistics_3)
    # Level 4
    level_cost_4 = Resources()
    level_cost_4.Init(600, 8, 8, 1, 8)
    Fortress.cost_per_level.append(level_cost_4)
    level_production_4 = Resources()
    level_production_4.Init(50, 2, 2)
    Fortress.production_per_level.append(level_production_4)
    level_statistics_4 = Statistics()
    level_statistics_4.Init(600, 16, 5, 5, 6, 6)
    Fortress.statistics_per_level.append(level_statistics_4)
    # Level 5
    level_cost_5 = Resources()
    level_cost_5.Init(800, 9, 9, 1, 12)
    Fortress.cost_per_level.append(level_cost_5)
    level_production_5 = Resources()
    level_production_5.Init(60, 2, 2)
    Fortress.production_per_level.append(level_production_5)
    level_statistics_5 = Statistics()
    level_statistics_5.Init(600, 16, 5, 5, 7, 7)
    Fortress.statistics_per_level.append(level_statistics_5)
    # Level 6
    level_cost_6 = Resources()
    level_cost_6.Init(1200, 10, 10, 2, 14)
    Fortress.cost_per_level.append(level_cost_6)
    level_production_6 = Resources()
    level_production_6.Init(80, 2, 2)
    Fortress.production_per_level.append(level_production_6)
    level_statistics_6 = Statistics()
    level_statistics_6.Init(700, 17, 6, 6, 7, 7)
    Fortress.statistics_per_level.append(level_statistics_6)
    # Level 7
    level_cost_7 = Resources()
    level_cost_7.Init(1500, 10, 10, 2, 16)
    Fortress.cost_per_level.append(level_cost_7)
    level_production_7 = Resources()
    level_production_7.Init(90, 2, 2, 1)
    Fortress.production_per_level.append(level_production_7)
    level_statistics_7 = Statistics()
    level_statistics_7.Init(800, 18, 7, 7, 7, 7)
    Fortress.statistics_per_level.append(level_statistics_7)
    # Level 8
    level_cost_8 = Resources()
    level_cost_8.Init(2000, 12, 12, 3, 20)
    Fortress.cost_per_level.append(level_cost_8)
    level_production_8 = Resources()
    level_production_8.Init(100, 2, 2, 1, 1)
    Fortress.production_per_level.append(level_production_8)
    level_statistics_8 = Statistics()
    level_statistics_8.Init(900, 19, 7, 7, 7, 7)
    Fortress.statistics_per_level.append(level_statistics_8)

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
    if inspect.isclass(building):
        Utility.SendMsg(player, Colors.COLOR_AZURE + building.__name__ + ": \n")
        Utility.SendMsg(player, building.ExtraInfo())
    else:
        Utility.SendMsg(player, Colors.COLOR_AZURE + building.__class__.__name__ + ": \n")
        Utility.SendMsg(player, building.__class__.ExtraInfo())
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
        actualTime = time.localtime(time.time())
        if building.LastGathered.tm_year < actualTime.tm_year or \
            building.LastGathered.tm_mon < actualTime.tm_mon or \
            building.LastGathered.tm_mday < actualTime.tm_mday or \
            building.LastGathered.tm_hour + 5 < actualTime.tm_hour:
            building.LastGathered = actualTime
            for iType, iAmount in building.production.iteritems():
                if iAmount > 0:
                    resource[iType] += iAmount
    return resource

class Building(object):
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        if len(args) > 0:
            obj.owner = args[0].username
            obj.owner_info = args[0].info
            obj.LastGathered = time.localtime(time.time() - 60*60*6)
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
        
    cost_per_level = []
    cost = Resources()
    cost.Init(500, 10, 10, 2)
    
    production_per_level = []
    production = Resources()
    production.Init(20, 1, 1)
    
    statistics_per_level = []
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
        self.owner_info.maxNumberOfUnits += self.army_production
        
    def __del__(self):
        self.owner_info.maxNumberOfUnits -= self.army_production
    
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
    cost.Init(60, 3, 3)
    
    statistics = Statistics()
    statistics.Init(120, 4)
      
    army_production = 5
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = copy(self.__class__.statistics)
        
        self.army_production = self.__class__.army_production
        self.owner_info.maxNumberOfUnits += self.army_production
    
    def __del__(self):
        self.owner_info.maxNumberOfUnits -= self.army_production   
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Each house provide you to recruit more army.\n"
        return extraInfoMsg

class Bank(Building):
    field = "B" 
    color = Colors.COLOR_GOLD
    
    cost = Resources()
    cost.Init(50, 6, 6)
    
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
    cost.Init(60, 0, 6)
    
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
    cost.Init(60, 6)
    
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
    cost.Init(30, 1, 1)
    
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
    cost.Init(250, 5, 5, 1)
    
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
    cost.Init(200, 4, 4, 1)
    
    production = Resources()
    production.Init(0, 0, 0, 0, 1)
    
    statistics = Statistics()
    statistics.Init(50, 4)  
        
    def __init__(self, player):
        self.field = self.__class__.field
        self.color = self.__class__.color
        self.statistics = copy(self.__class__.statistics)
        self.production = self.__class__.production
    
    @staticmethod
    def ExtraInfo():
        extraInfoMsg = Colors.COLOR_GREEN
        extraInfoMsg += "Each library provide you science points.\n"
        return extraInfoMsg