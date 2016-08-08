from Colors import Colors
from Commands import WorldMapCommands
from Commands import MainCommands
from Database import Database
from Pos import Pos
from Data import mainData
from Data import dbLock
from Map import mainMap as Map
import Attack
import Config
import re
import LocalMap
import Buildings
import Utility
import State
import Control
import Log
import Geo
import Scout

def LoadMap():
    Log.Save("LoadMap.\n")
    inputFile = open(Config.mapPath, 'r')
    data = inputFile.readlines()
    Map.y_size = len(data)
    Map.x_size = len(data[0].replace("\n", ""))
    
    for y in range(Map.y_size * Map.end):
        row = []; y
        for x in range(Map.x_size * Map.end):
            row.append(Buildings.Empty()); x
        Map.fields.append(row) 
    with dbLock:   
        mainData.map = Map
        Database.SaveDatabase()
        
def LoadMapFromDb():
    Log.Save("LoadMapFromDb.\n")
    with dbLock:   
        Map.Load(mainData.map)                
        
def InitForbiddenPlaces():
    Log.Save("InitForbiddenPlaces.\n")
    for wy in range(Map.y_size):
        for wx in range(Map.x_size):
            for y in range(Map.firstQ):
                for x in range(Map.firstQ):
                    Map.SetForbidden(Pos(wy, wx, y, x))
            for y in range(Map.firstQ):
                for x in range(Map.thirdQ, Map.end):
                    Map.SetForbidden(Pos(wy, wx, y, x))
            for y in range(Map.thirdQ, Map.end):
                for x in range(Map.firstQ):
                    Map.SetForbidden(Pos(wy, wx, y, x))
            for y in range(Map.thirdQ, Map.end):
                for x in range(Map.thirdQ, Map.end):
                    Map.SetForbidden(Pos(wy, wx, y, x))

def ParseCommand(player, command):
    try:
        y, x = map(int, re.findall(r'\d+', command))
        if 0 <= x < Map.x_size and 0 <= y < Map.y_size: 
            return True, y, x
        else:
            if not 0 <= x < Map.x_size:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value X out of range! X must be in range: 0 - " + str(Map.x_size-1) + "\n")
                return False, 0, 0
            if not 0 <= y < Map.y_size:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value Y out of range! Y must be in range: 0 - " + str(Map.y_size-1) + "\n")
                return False, 0, 0   
    except ValueError:
        Utility.SendMsg(player, Colors.COLOR_RED + \
                        "Bad number of arguments! Provide exactly two arguments!\n")  
        return False, 0, 0
    
def ParseCommandThree(player, command):
    try:
        y, x = map(int, re.findall(r'\d+', command))
        geo = re.findall(r'\w$', command)[0]
        if 0 <= x < Map.x_size and 0 <= y < Map.y_size and "NSEW".find(geo) != -1: 
            return True, y, x, geo
        else:
            if not 0 <= x < Map.x_size:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value X out of range! X must be in range: 0 - " + str(Map.x_size-1) + "\n")
                return False, 0, 0, 0
            if not 0 <= y < Map.y_size:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value Y out of range! Y must be in range: 0 - " + str(Map.y_size-1) + "\n")
                return False, 0, 0, 0   
            Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Wrong direction! Possible directions are: N, S, E, W\n")
            return False, 0, 0, 0
            
    except ValueError:
        Utility.SendMsg(player, Colors.COLOR_RED + \
                        "Bad number of arguments! Provide exactly three arguments!\n")  
        return False, 0, 0, 0
    
def ExecuteCommand(player, command):
    # MainCommands >>>
    if command == MainCommands._0_0_SHOW_MAP:
        ShowMap(player)
    elif command == MainCommands._1_0_SHOW_RESOURCES:
        player.ShowResources()
    elif command == MainCommands._2_0_RETURN:
        Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to Main Menu!\n")
        player.state = State.INIT
        player.loggedIn = False
    elif command == MainCommands._3_0_EXIT:
        Utility.SendMsg(player, Control.CTRL_EXIT)
        player.state = State.EXITING
    # MainCommands <<<     
    elif command == WorldMapCommands._3_0_GET_PRODUCTION:
        GetProduction(player)
    elif command == WorldMapCommands._0_0_SHOW_FORTRESS_INFO:
        Buildings.ShowInfo(player, Buildings.Fortress)
    elif command.find(WorldMapCommands._1_2_SETTLE_FORTRESS) == 0 or \
         command.find(WorldMapCommands._2_2_ENTER_FORTRESS) == 0 or \
         command.find(WorldMapCommands._4_2_ATTACK_FORTRESS) == 0 or \
         command.find(WorldMapCommands._5_2_REPAIR_FORTRESS) == 0:
        succes, wy, wx = ParseCommand(player, command)
        if succes:
            if command.find(WorldMapCommands._1_2_SETTLE_FORTRESS) == 0:
                SettleFortress(player, wy, wx)
            elif command.find(WorldMapCommands._2_2_ENTER_FORTRESS) == 0:
                EnterFortress(player, wy, wx)
            elif command.find(WorldMapCommands._4_2_ATTACK_FORTRESS) == 0:
                AttackFortress(player, wy, wx)
            elif command.find(WorldMapCommands._5_2_REPAIR_FORTRESS) == 0:
                RepairFortress(player, wy, wx)
    elif command.find(WorldMapCommands._6_3_MOVE_ARMY) == 0:
        succes, wy, wx, geo = ParseCommandThree(player, command)
        if succes:
            MoveArmy(player, wy, wx, geo)
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Undefined command! Try again!\n")
  
def ShowMap(player):
    mapMsg = Colors.COLOR_WHITE
    row, col = 0, 0
    mapMsg += "  "
    for x in range(Map.x_size):
        if col < 10:
            mapMsg += " "
        mapMsg += str(col)
        mapMsg += " "
        col += 1; x
    mapMsg += "\n"
    for wy in range(Map.y_size):
        if row < 10:
            mapMsg += " "
        mapMsg += str(row)
        row += 1
        for wx in range(Map.x_size):  
            field = Map.GetFort(wy, wx)
            mapMsg += " "
            if Config.randomColors:
                if field is not None:
                    mapMsg += field.owner_info.color + str(field.level)
                else:
                    mapMsg += Buildings.Empty.color + Buildings.Empty.field
            else:
                if field is not None:
                    if field.owner == player.username:
                        mapMsg += Colors.COLOR_GREEN 
                    else:
                        mapMsg += Colors.COLOR_RED
                    mapMsg += str(field.level)
                else:
                    mapMsg += Buildings.Empty.color + Buildings.Empty.field
            mapMsg += Colors.COLOR_WHITE + " "
        mapMsg += "\n\n"    
    Utility.SendMsg(player, mapMsg)   

def SettleFortress(player, wy, wx):
    if not isinstance(Map.GetFort(wy, wx), Buildings.Fortress):
        if player.Pay(Buildings.Fortress.cost, 100):   
            Log.Save(player.username + " construct new fortress on " + str(wy) + " " + str(wx) + "!\n")
            Map.SetFort(player, wy, wx)
            Utility.SendMsg(player, Colors.COLOR_GREEN + "Fortress successfully settled!\n") 
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Not enough resources!\n") 
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Field is not empty!\n")
          
def EnterFortress(player, wy, wx):
    fort = Map.GetFort(wy, wx)
    if fort is not None:
        player.wy = wy
        player.wx = wx
        if fort.owner == player.username:
            player.state = State.LOCAL_MAP
        else:
            Scout.ScoutingMode(player)
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Field is empty!\n")
        
def GetProduction(player):
    for wy in range(Map.y_size):
        for wx in range(Map.x_size):
            fort = Map.GetFort(wy, wx)
            if isinstance(fort, Buildings.Fortress) and fort.owner == player.username:
                LocalMap.GetProduction(player, wy, wx)  
    Utility.SendMsg(player, Colors.COLOR_GREEN + "All production gathered!\n")   
        
def AttackFortress(player, wy ,wx):
    fort = Map.GetFort(wy, wx)
    if fort is not None:
        if fort.owner != player.username:
            player.wy = wy
            player.wx = wx   
            if Attack.AttackFortress(player, wy, wx):
                LocalMap.OvertakeFortress(player, wy, wx)
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Can't attack own fortress!\n")
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Field is empty!\n")
    
def RepairFortress(player, wy ,wx):
    fort = Map.GetFort(wy, wx)
    if fort is not None:
        if fort.owner == player.username:
            player.wy = wy
            player.wx = wx 
            if not LocalMap.RepairFortress(player):
                Utility.SendMsg(player, Colors.COLOR_RED + "Nothing to repair!\n")
            else:
                Log.Save(player.username + " repair fortress!\n")
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Can't repair enemy fortress!\n")
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Field is empty!\n")
        
def MoveArmy(player, wy, wx, geo):
    Log.Save(player.username + " try to move army\n")
    fort = Map.GetFort(wy, wx)
    if fort is not None:
        if fort.owner == player.username:
            if geo == Geo.NORTH:
                dest_fort = Map.GetFort(wy-1, wx)
            elif geo == Geo.SOUTH:
                dest_fort = Map.GetFort(wy+1, wx)
            elif geo == Geo.EAST:
                dest_fort = Map.GetFort(wy, wx+1)
            elif geo == Geo.WEST:
                dest_fort = Map.GetFort(wy, wx-1)
            if dest_fort is not None:
                if dest_fort.owner == player.username:
                    LocalMap.MoveUnits(player, wy, wx, geo)
                else:
                    Utility.SendMsg(player, Colors.COLOR_RED + "Can't move units into enemy fortress!\n")
            else:
                Utility.SendMsg(player, Colors.COLOR_RED + "Can't move units into empty field!\n")
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Can't move units on enemy fortress!\n")
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Field is empty!\n") 
    