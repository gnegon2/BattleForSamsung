from Colors import Colors
import Commands
from Commands import MainCommands, BuildingCommands
from Commands import LocalMapCommands
from Commands import ActionCommands
from Commands import UnitsCommands
from Pos import Pos
import Buildings
import Units
import Utility
import Control
import State
import Config
import re
import time
import Map
 
def ParseCommandXY(player, command):
    try:
        y, x = map(int, re.findall(r'\d+', command))
        if 0 <= x < Map.end and 0 <= y < Map.end:
            return True, y, x
        else:
            if not 0 <= x < Map.end:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value X out of range! X must be in range: 0 - " + str(Map.end - 1) + "\n")
                return False, 0, 0
            if not 0 <= y < Map.end:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value Y out of range! Y must be in range: 0 - " + str(Map.end - 1) + "\n")
                return False, 0, 0
    except ValueError:
        Utility.SendMsg(player, Colors.COLOR_RED + "Bad number of arguments! Provide exactly two arguments!\n")
        return False, 0, 0
 
def ExecuteCommand(player, command):
    # MainCommands >>>
    if command == MainCommands._0_0_SHOW_MAP:
        ShowMap(player)
    elif command == MainCommands._1_0_SHOW_RESOURCES:
        player.ShowResources()
    elif command == MainCommands._2_0_RETURN:
        Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to World Map!\n")
        player.state = State.WORLD_MAP
    elif command == MainCommands._3_0_EXIT:
        Utility.SendMsg(player, Control.CTRL_EXIT)
        player.state = State.EXITING
    # MainCommands <<<   
    elif command == LocalMapCommands._0_0_BUILDINGS:
        BuildingMenu(player)
    elif command == LocalMapCommands._1_0_ARMY:
        UnitsMenu(player)
    elif command.find(LocalMapCommands._2_2_DESTROY) != -1:
        Destroy(player, command)
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Undefined command!\n")
   
def ShowMap(player):     
    row, col = 0, 0
    mapMsg = Colors.COLOR_WHITE + "  "
    for x in range(Map.end):
        if col < 10:
            mapMsg += " "
        mapMsg += Colors.COLOR_WHITE + str(col)
        mapMsg += " "
        col += 1
    mapMsg += "\n"
    for y in range(Map.end):
        if row < 10:
            mapMsg += " "
        mapMsg += Colors.COLOR_WHITE + str(row)
        row += 1
        for x in range(0, Map.end):   
            instance = Map.Get(Pos(player.wy, player.wx, y, x))
            mapMsg += " "
            mapMsg += instance.color + instance.field
            mapMsg += " "
        mapMsg += "\n\n"
    Utility.SendMsg(player, mapMsg)

def BuildingMenu(player):
    buildingMenu = Colors.COLOR_AZURE
    buildingMenu += "Welcome in Building Menu!\n"
    buildingMenu += "available options are:\n"
    Utility.SendMsg(player, buildingMenu)
    Utility.SendMsg(player, Commands.GetCommands(BuildingCommands))
    Utility.SendMsg(player, Commands.GetCommands(MainCommands))
    
    
    player.state = State.BUILDING_MENU
    while player.state == State.BUILDING_MENU:
        Utility.SendMsg(player, Control.CTRL_MENU_BUILDING)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        # MainCommands >>>
        if command == MainCommands._0_0_SHOW_MAP:
            ShowMap(player)
        elif command == MainCommands._1_0_SHOW_RESOURCES:
            player.ShowResources()
        elif command == MainCommands._2_0_RETURN:
            player.state = State.LOCAL_MAP
            Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to Local Map!\n")
        elif command == MainCommands._3_0_EXIT:
            Utility.SendMsg(player, Control.CTRL_EXIT)
            player.state = State.EXITING
        # MainCommands <<<
        else:
            building = Buildings.CommandToBuilding(command)
            if isinstance(building, Buildings.Empty):
                Utility.SendMsg(player, Colors.COLOR_RED + "Undefined building!\n")
            else:
                BuildingActionMenu(player, building)

def BuildingActionMenu(player, building):
    actionsMenu = Colors.COLOR_AZURE
    actionsMenu += "available actions on buildings are:\n"
    Utility.SendMsg(player, actionsMenu)
    Utility.SendMsg(player, Commands.GetCommands(ActionCommands))
    Utility.SendMsg(player, Commands.GetCommands(MainCommands))
    
    player.state = State.BUILDING_ACTION_MENU
    while player.state == State.BUILDING_ACTION_MENU:
        Utility.SendMsg(player, Control.CTRL_MENU_ACTION)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        # MainCommands >>>
        if command == MainCommands._0_0_SHOW_MAP:
            ShowMap(player)
        elif command == MainCommands._1_0_SHOW_RESOURCES:
            player.ShowResources()
        elif command == MainCommands._2_0_RETURN:
            player.state = State.BUILDING_MENU
            Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to Building Menu!\n")
        elif command == MainCommands._3_0_EXIT:
            Utility.SendMsg(player, Control.CTRL_EXIT)
            player.state = State.EXITING
        # MainCommands <<<
        elif command == ActionCommands._0_0_SHOW_INFO:
                Buildings.ShowInfo(player, building)
        elif command.find(ActionCommands._1_2_CREATE) == 0:
            succes, y, x = ParseCommandXY(player, command)
            if succes:
                CreateBuilding(player, building, y, x)
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Undefined action!\n")

def CreateBuilding(player, building, y, x):
    CheckLastBuild(player)
    if player.info.buildingsBuildToday < Config.maxBuildingsPerDay:
        pos = Pos(player.wy, player.wx, y, x)
        field = Map.Get(pos)
        if isinstance(field, Buildings.Empty):
            if Buildings.Pay(player, building): 
                Map.Set(player, building, pos)
                Utility.SendMsg(player, Colors.COLOR_GREEN + "Building created!\n") 
            else:
                Utility.SendMsg(player, Colors.COLOR_RED + "Not enough resources!\n") 
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Field is not empty!\n") 
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "You have built maximum buildings today!\n")     
        
def CheckLastBuild(player):
    actualTime = time.localtime(time.time())
    if player.info.LastBuild.tm_year < actualTime.tm_year or \
        player.info.LastBuild.tm_mon < actualTime.tm_mon or \
        player.info.LastBuild.tm_mday < actualTime.tm_mday or \
        player.info.LastBuild.tm_min + 5 < actualTime.tm_min:
            player.info.LastBuild = actualTime
            player.info.buildingsBuildToday = 0
        
def GetProduction(player, wy, wx):
    fort = Map.GetFort(wy, wx)
    for y in range(Map.end):
        for x in range(Map.end):
            building = Map.Get(Pos(wy, wx, y, x))
            if isinstance(building, Buildings.Building) and \
                not isinstance(building, Buildings.Fortress):
                Buildings.GetProduction(player, building)
                                 
def UnitsMenu(player):
    level = Map.GetFort(player.wy, player.wx).level
    
    unitsMenu = Colors.COLOR_AZURE
    unitsMenu += "Welcome in Units Menu!\n"
    unitsMenu += "available options are:\n"
    Utility.SendMsg(player, unitsMenu)
    Utility.SendMsg(player, Commands.GetUnitCommands(level))
    Utility.SendMsg(player, Commands.GetCommands(MainCommands))
    
    player.state = State.UNITS_MENU
    while player.state == State.UNITS_MENU:
        Utility.SendMsg(player, Control.CTRL_MENU_UNITS + str(level))
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        # MainCommands >>>
        if command == MainCommands._0_0_SHOW_MAP:
            ShowMap(player)
        elif command == MainCommands._1_0_SHOW_RESOURCES:
            player.ShowResources()
        elif command == MainCommands._2_0_RETURN:
            player.state = State.LOCAL_MAP
            Utility.SendMsg(player, Control.CTRL_MENU_LOCAL_MAP)
            Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to Local Map!\n")
        elif command == MainCommands._3_0_EXIT:
            Utility.SendMsg(player, Control.CTRL_EXIT)
            player.state = State.EXITING
        # MainCommands <<<
        elif command.find(UnitsCommands._0_4_MOVE_UNIT) != -1:
            MoveUnit(player, command)
        else:
            unit = Units.CommandToUnit(command)
            print unit
            if unit is Units.Empty:
                Utility.SendMsg(player, Colors.COLOR_RED + "Undefined unit!\n")
            else:
                UnitsActionMenu(player, unit)
                
def UnitsActionMenu(player, unit):  
    actionsMenu = Colors.COLOR_AZURE
    actionsMenu += "available actions on units are:\n"
    Utility.SendMsg(player, actionsMenu)  
    Utility.SendMsg(player, Commands.GetCommands(ActionCommands))
    Utility.SendMsg(player, Commands.GetCommands(MainCommands))   
    
    player.state = State.UNITS_ACTION_MENU
    while player.state == State.UNITS_ACTION_MENU:
        Utility.SendMsg(player, Control.CTRL_MENU_ACTION)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        # MainCommands >>>
        if command == MainCommands._0_0_SHOW_MAP:
            ShowMap(player)
        elif command == MainCommands._1_0_SHOW_RESOURCES:
            player.ShowResources()
        elif command == MainCommands._2_0_RETURN:
            player.state = State.UNITS_MENU
            Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to Units Menu!\n")
        elif command == MainCommands._3_0_EXIT:
            Utility.SendMsg(player, Control.CTRL_EXIT)
            player.state = State.EXITING
        # MainCommands <<<
        elif command == ActionCommands._0_0_SHOW_INFO:
            Units.ShowInfo(player, unit)
        elif command.find(ActionCommands._1_2_CREATE) == 0:
            succes, y, x = ParseCommandXY(player, command)
            if succes:
                RecruitUnit(player, unit, y, x) 
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Undefined action!\n")
                
def RecruitUnit(player, unit, y, x):
    CheckLastRecruit(player)
    if player.info.numberOfUnits <= player.info.maxNumberOfUnits:
        if player.info.unitsRecruitedToday < Config.maxUnitsPerDay:
            pos = Pos(player.wy, player.wx, y, x)
            field = Map.Get(pos)
            if isinstance(field, Buildings.Empty):
                if Units.Buy(player, unit):
                    player.info.unitsRecruitedToday += 1
                    Map.Set(player, unit, pos)
                    Utility.SendMsg(player, Colors.COLOR_GREEN + "Unit recruited!\n") 
                else:
                    Utility.SendMsg(player, Colors.COLOR_RED + "Not enough resources!\n") 
            else:
                Utility.SendMsg(player, Colors.COLOR_RED + "Field is not empty!\n") 
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "You have recruit maximum units today!\n")   
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "You have recruit maximum units!\nBuild new houses to recruit more!\n")  

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
        pos = Pos(player.wy, player.wx, y, x)
        field = Map.Get(pos)
        if not isinstance(field, Buildings.Fortress):
            if isinstance(field, Buildings.Building) or isinstance(field, Units.Unit):
                Map.SetEmpty(pos)
                Utility.SendMsg(player, Colors.COLOR_GREEN + "Succesfully destroyed!\n")
            else:
                Utility.SendMsg(player, Colors.COLOR_RED + "This field can't be destroyed!\n")
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Fortress can't be destroyed!\n")
               
def ParseCommandFour(player, command):
    try:
        y1, x1, y2, x2, = map(int, re.findall(r'\d+', command))
        if 0 <= x1 < Map.end and 0 <= y1 < Map.end and \
           0 <= x2 < Map.end and 0 <= y2 < Map.end: 
            return True, y1, x1, y2, x2
        else:
            if not 0 <= x1 < Map.end:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value X1 out of range! X1 must be in range: 0 - " + str(Map.end - 1) + "\n")
                return False, 0, 0
            if not 0 <= x2 < Map.end:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value X2 out of range! X2 must be in range: 0 - " + str(Map.end - 1) + "\n")
                return False, 0, 0
            if not 0 <= y1 < Map.end:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value Y1 out of range! Y1 must be in range: 0 - " + str(Map.end - 1) + "\n")
                return False, 0, 0
            if not 0 <= y2 < Map.end:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value Y2 out of range! Y2 must be in range: 0 - " + str(Map.end - 1) + "\n")
                return False, 0, 0
    except ValueError:
        Utility.SendMsg(player, Colors.COLOR_RED + "Bad number of arguments! Provide exactly four arguments!\n")
        return False, 0, 0, 0, 0

def MoveUnit(player, command):        
    succes, y1, x1, y2, x2, = ParseCommandFour(player, command)
    if succes:
        pos2 = Pos(player.wy, player.wx, y2, x2)
        field2 = Map.Get(pos2)
        pos1 = Pos(player.wy, player.wx, y1, x1)
        field1 = Map.Get(pos1)
        if isinstance(field2, Buildings.Empty):
            if isinstance(field1, Units.Unit):
                Map.Swap(pos1, pos2)
                Utility.SendMsg(player, Colors.COLOR_GREEN + "Unit succesfully moved!\n")
            else:
                Utility.SendMsg(player, Colors.COLOR_RED + "Only units can be moved!\n") 
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Destination place is not empty!\n")     
