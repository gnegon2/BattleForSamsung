import Buildings
import Units
import Utility
import Control
import State
from Commands import MainCommands
from Commands import LocalMapCommands
from Commands import BuildingCommands
from Commands import ActionCommands
from Commands import UnitsCommands
from LocalMapStruct import localMaps
import Config
import re
import time

def InitMap(player, y, x):        
    localMapStruct = localMaps[y][x]
    localMapStruct.fields[Config.localMapSize / 2 - 1][Config.localMapSize / 2 - 1] = Buildings.Fortress(player)
    localMapStruct.fields[Config.localMapSize / 2 - 1][Config.localMapSize / 2] = Buildings.Fortress(player)
    localMapStruct.fields[Config.localMapSize / 2][Config.localMapSize / 2 - 1] = Buildings.Fortress(player)
    localMapStruct.fields[Config.localMapSize / 2][Config.localMapSize / 2] = Buildings.Fortress(player)
 
def ParseCommandXY(player, command):
    try:
        y, x = map(int, re.findall(r'\d+', command))
        if 0 <= x < Config.localMapSize and 0 <= y < Config.localMapSize:
            return True, y, x
        else:
            if not 0 <= x < Config.localMapSize:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + \
                                "Value X out of range! X must be in range: 0 - " + str(Config.localMapSize - 1) + "\n")
                return False, 0, 0
            if not 0 <= y < Config.localMapSize:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + \
                                "Value Y out of range! Y must be in range: 0 - " + str(Config.localMapSize - 1) + "\n")
                return False, 0, 0
    except ValueError:
        Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Bad number of arguments! Provide exactly two arguments!\n")
        return False, 0, 0
 
def ExecuteCommand(player, command):
    # MainCommands >>>
    if command == MainCommands.SHOW_MAP:
        ShowMap(player)
    elif command == MainCommands.SHOW_RESOURCES:
        player.ShowResources()
    elif command == MainCommands.RETURN:
        Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Returning to World Map!\n")
        player.state = State.WORLD_MAP
    elif command == MainCommands.EXIT:
        Utility.SendMsg(player, Control.CTRL_EXIT)
        player.state = State.EXITING
    # MainCommands <<<   
    elif command == LocalMapCommands.BUILDINGS:
        BuildingMenu(player)
    elif command == LocalMapCommands.ARMY:
        UnitsMenu(player)
    elif command.find(LocalMapCommands.DESTROY) != -1:
        Destroy(player, command)
    else:
        Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Undefined command!\n")
   
def ShowMap(player):     
    localMapStruct = localMaps[player.localMapY][player.localMapX]
    row, col = 0, 0
    mapMsg = Control.CTRL_COLOR_WHITE + "  "
    for x in range(0, Config.localMapSize):
        if col < 10:
            mapMsg += " "
        mapMsg += Control.CTRL_COLOR_WHITE + str(col)
        mapMsg += " "
        col += 1
    mapMsg += "\n"
    for y in range(0, Config.localMapSize):
        if row < 10:
            mapMsg += " "
        mapMsg += Control.CTRL_COLOR_WHITE + str(row)
        row += 1
        for x in range(0, Config.localMapSize):   
            instance = localMapStruct.fields[y][x]
            mapMsg += " "
            mapMsg += instance.color + instance.field
            mapMsg += " "
        mapMsg += "\n\n"
    Utility.SendMsg(player, mapMsg)

def BuildingMenu(player):
    buildingMenu = Control.CTRL_COLOR_AZURE
    buildingMenu += "Welcome in Building Menu!\n"
    buildingMenu += "available options are:\n"
    Utility.SendMsg(player, buildingMenu)
    Utility.SendMsg(player, BuildingCommands.Get())
    Utility.SendMsg(player, MainCommands.Get())
    
    player.state = State.BUILDING_MENU
    while player.state == State.BUILDING_MENU:
        Utility.SendMsg(player, Control.CTRL_BUILDING_MENU)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        # MainCommands >>>
        if command == MainCommands.SHOW_MAP:
            ShowMap(player)
        elif command == MainCommands.SHOW_RESOURCES:
            player.ShowResources()
        elif command == MainCommands.RETURN:
            player.state = State.LOCAL_MAP
            Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Returning to Local Map!\n")
        elif command == MainCommands.EXIT:
            Utility.SendMsg(player, Control.CTRL_EXIT)
            player.state = State.EXITING
        # MainCommands <<<
        else:
            building = Buildings.CommandToBuilding(command)
            if isinstance(building, Buildings.Empty):
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Undefined building!\n")
            else:
                BuildingActionMenu(player, building)

def BuildingActionMenu(player, building):
    actionsMenu = Control.CTRL_COLOR_AZURE
    actionsMenu += "available actions on buildings are:\n"
    Utility.SendMsg(player, actionsMenu)
    Utility.SendMsg(player, ActionCommands.Get())
    Utility.SendMsg(player, MainCommands.Get())
    
    player.state = State.BUILDING_ACTION_MENU
    while player.state == State.BUILDING_ACTION_MENU:
        Utility.SendMsg(player, Control.CTRL_BUILDING_ACTION_MENU)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        # MainCommands >>>
        if command == MainCommands.SHOW_MAP:
            ShowMap(player)
        elif command == MainCommands.SHOW_RESOURCES:
            player.ShowResources()
        elif command == MainCommands.RETURN:
            player.state = State.BUILDING_MENU
            Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Returning to Building Menu!\n")
        elif command == MainCommands.EXIT:
            Utility.SendMsg(player, Control.CTRL_EXIT)
            player.state = State.EXITING
        # MainCommands <<<
        elif command == ActionCommands.SHOW_INFO:
                Buildings.ShowInfo(player, building)
        elif command.find(ActionCommands.CREATE) == 0:
            succes, y, x = ParseCommandXY(player, command)
            if succes:
                CreateBuilding(player, building, y, x)
        else:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Undefined action!\n")

def CreateBuilding(player, building, y, x):
    CheckLastBuild(player)
    if player.info.buildingsBuildToday < Config.maxBuildingsPerDay:
        localMapStruct = localMaps[player.localMapY][player.localMapX]
        if isinstance(localMapStruct.fields[y][x], Buildings.Empty):
            if Buildings.Build(player, building): 
                player.info.buildingsBuildToday += 1
                print "player.info.buildingsBuildToday=" + str(player.info.buildingsBuildToday)
                localMapStruct.fields[y][x] = building(player)
                Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Building created!\n") 
            else:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Not enough resources!\n") 
        else:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Field is not empty!\n") 
    else:
        Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You have built maximum buildings today!\n")     
 
def CheckLastBuild(player):
    actualTime = time.localtime(time.time())
    if player.info.LastBuild.tm_year < actualTime.tm_year or \
        player.info.LastBuild.tm_mon < actualTime.tm_mon or \
        player.info.LastBuild.tm_mday < actualTime.tm_mday or \
        player.info.LastBuild.tm_min + 5 < actualTime.tm_min:
            player.info.LastBuild = actualTime
            player.info.buildingsBuildToday = 0
        
def GetProduction(player, y, x):
    localMapStruct = localMaps[y][x]
    for y in range(0, Config.localMapSize):
        for x in range(0, Config.localMapSize):
            building = localMapStruct.fields[y][x]
            if isinstance(building, Buildings.Building):
                Buildings.GetProduction(player, building)
                                 
def UnitsMenu(player):
    level = localMaps[player.localMapY][player.localMapX].librariesCount
    
    unitsMenu = Control.CTRL_COLOR_AZURE
    unitsMenu += "Welcome in Units Menu!\n"
    unitsMenu += "available options are:\n"
    Utility.SendMsg(player, unitsMenu)
    Utility.SendMsg(player, UnitsCommands.Get(level))
    Utility.SendMsg(player, MainCommands.Get())
    
    player.state = State.UNITS_MENU
    while player.state == State.UNITS_MENU:
        
        Utility.SendMsg(player, Control.CTRL_UNITS_MENU + str(level))
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        # MainCommands >>>
        if command == MainCommands.SHOW_MAP:
            ShowMap(player)
        elif command == MainCommands.SHOW_RESOURCES:
            player.ShowResources()
        elif command == MainCommands.RETURN:
            player.state = State.LOCAL_MAP
            Utility.SendMsg(player, Control.CTRL_LOCAL_MAP)
            Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Returning to Local Map!\n")
        elif command == MainCommands.EXIT:
            Utility.SendMsg(player, Control.CTRL_EXIT)
            player.state = State.EXITING
        # MainCommands <<<
        elif command.find(UnitsCommands.MOVE_UNIT) != -1:
            MoveUnit(player, command)
        else:
            unit = Units.CommandToUnit(player, command)
            if isinstance(unit, Units.Empty):
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Undefined unit!\n")
            else:
                UnitsActionMenu(player, unit)
                
def UnitsActionMenu(player, unit):  
    actionsMenu = Control.CTRL_COLOR_AZURE
    actionsMenu += "available actions on units are:\n"
    Utility.SendMsg(player, actionsMenu)     
    Utility.SendMsg(player, ActionCommands.Get())
    Utility.SendMsg(player, MainCommands.Get())
    
    player.state = State.UNITS_ACTION_MENU
    while player.state == State.UNITS_ACTION_MENU:
        Utility.SendMsg(player, Control.CTRL_UNITS_ACTION_MENU)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        # MainCommands >>>
        if command == MainCommands.SHOW_MAP:
            ShowMap(player)
        elif command == MainCommands.SHOW_RESOURCES:
            player.ShowResources()
        elif command == MainCommands.RETURN:
            player.state = State.UNITS_MENU
            Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Returning to Units Menu!\n")
        elif command == MainCommands.EXIT:
            Utility.SendMsg(player, Control.CTRL_EXIT)
            player.state = State.EXITING
        # MainCommands <<<
        elif command == ActionCommands.SHOW_INFO:
            Units.ShowInfo(player, unit)
        elif command.find(ActionCommands.CREATE) == 0:
            succes, y, x = ParseCommandXY(player, command)
            if succes:
                RecruitUnit(player, unit, y, x) 
        else:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Undefined action!\n")
                
def RecruitUnit(player, unit, y, x):
    CheckLastRecruit(player)
    if player.info.numberOfUnits <= player.info.maxNumberOfUnits:
        if player.info.unitsRecruitedToday < Config.maxUnitsPerDay:
            localMapStruct = localMaps[player.localMapY][player.localMapX]
            if isinstance(localMapStruct.fields[y][x], Buildings.Empty):
                if Units.Buy(player, unit):
                    player.info.unitsRecruitedToday += 1
                    localMapStruct.fields[y][x] = unit(player)
                    Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Unit recruited!\n") 
                else:
                    Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Not enough resources!\n") 
            else:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Field is not empty!\n") 
        else:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You have recruit maximum units today!\n")   
    else:
        Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You have recruit maximum units!\nBuild new houses to recruit more!\n")  

def CheckLastRecruit(player):
    actualTime = time.localtime(time.time())
    if player.info.LastRecruit.tm_year < actualTime.tm_year or \
        player.info.LastRecruit.tm_mon < actualTime.tm_mon or \
        player.info.LastRecruit.tm_mday < actualTime.tm_mday or \
        player.info.LastRecruit.tm_min + 5 < actualTime.tm_min:
            player.info.LastRecruit = actualTime
            player.info.unitsRecruitedToday = 0
        
def Destroy(player, command):
    succes, y, x = ParseCommandXY(player, command)
    if succes:
        localMapStruct = localMaps[player.localMapY][player.localMapX] 
        instance = localMapStruct.fields[y][x]
        if not isinstance(instance, Buildings.Fortress):
            if isinstance(instance, Buildings.Building) or isinstance(instance, Units.Unit):
                localMapStruct.fields[y][x] = Buildings.Empty()
                Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Succesfully destroyed!\n")
            else:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + "This field can't be destroyed!\n")
        else:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Fortress can't be destroyed!\n")
        
def ParseCommandFour(player, command):
    try:
        y1, x1, y2, x2, = map(int, re.findall(r'\d+', command))
        if 0 <= x1 < Config.localMapSize and 0 <= y1 < Config.localMapSize and \
           0 <= x2 < Config.localMapSize and 0 <= y2 < Config.localMapSize: 
            return True, y1, x1, y2, x2
        else:
            if not 0 <= x1 < Config.localMapSize:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + \
                                "Value X1 out of range! X1 must be in range: 0 - " + str(Config.localMapSize - 1) + "\n")
                return False, 0, 0
            if not 0 <= x2 < Config.localMapSize:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + \
                                "Value X2 out of range! X2 must be in range: 0 - " + str(Config.localMapSize - 1) + "\n")
                return False, 0, 0
            if not 0 <= y1 < Config.localMapSize:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + \
                                "Value Y1 out of range! Y1 must be in range: 0 - " + str(Config.localMapSize - 1) + "\n")
                return False, 0, 0
            if not 0 <= y2 < Config.localMapSize:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + \
                                "Value Y2 out of range! Y2 must be in range: 0 - " + str(Config.localMapSize - 1) + "\n")
                return False, 0, 0
    except ValueError:
        Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Bad number of arguments! Provide exactly four arguments!\n")
        return False, 0, 0, 0, 0

def MoveUnit(player, command):        
    succes, y1, x1, y2, x2, = ParseCommandFour(player, command)
    if succes:
        localMapStruct = localMaps[player.localMapY][player.localMapX]
        if isinstance(localMapStruct.fields[y2][x2], Buildings.Empty):
            if isinstance(localMapStruct.fields[y1][x1], Units.Unit):
                localMapStruct.fields[y2][x2] = localMapStruct.fields[y1][x1]
                localMapStruct.fields[y1][x1] = Buildings.Empty()
                Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Unit succesfully moved!\n")
            else:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Only units can be moved!\n") 
        else:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Destination place is not empty!\n")     
