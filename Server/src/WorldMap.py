from Colors import Colors
from Commands import WorldMapCommands, ScoutingCommands
from Commands import MainCommands
from Pos import Pos
import Attack
import Config
import re
import time
import LocalMap
import Buildings
import Utility
import State
import Control
import Log
import Map
import Commands

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
         command.find(WorldMapCommands._2_2_ENTER_FORTRESS) == 0:
        succes, wy, wx = ParseCommand(player, command)
        if succes:
            if command.find(WorldMapCommands._1_2_SETTLE_FORTRESS) == 0:
                SettleFortress(player, wy, wx)
            elif command.find(WorldMapCommands._2_2_ENTER_FORTRESS) == 0:
                EnterFortress(player, wy, wx)
    elif command.find(WorldMapCommands._4_2_ATTACK_FORTRESS) == 0:
        succes, wy, wx = ParseCommand(player, command)
        if succes:
            AttackFortress(player, wy, wx)
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
                if hasattr(field, 'owner'):
                    mapMsg += field.owner.info.color + str(field.level)
                else:
                    mapMsg += Buildings.Empty.color + Buildings.Empty.field
            else:
                if hasattr(field, 'owner'):
                    if field.owner == player:
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
        if Buildings.Pay(player, Buildings.Fortress):   
            Log.Save(player.username + " construct new fortress on " + str(wy) + " " + str(wx) + "!\n")
            Map.SetFort(player, wy, wx)
            Utility.SendMsg(player, Colors.COLOR_GREEN + "Fortress successfully settled!\n") 
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Not enough resources!\n") 
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Field is not empty!\n")
          
def EnterFortress(player, wy, wx):
    if isinstance(Map.GetFort(wy, wx), Buildings.Fortress):
        player.wy = wy
        player.wx = wx
        if Map.GetFort(wy, wx).owner == player:
            player.state = State.LOCAL_MAP
        else:
            ScoutingMode(player)
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Field is empty!\n")
        
def GetProduction(player):
    actualTime = time.localtime(time.time())
    if player.info.LastGathered.tm_year < actualTime.tm_year or \
        player.info.LastGathered.tm_mon < actualTime.tm_mon or \
        player.info.LastGathered.tm_mday < actualTime.tm_mday or \
        player.info.LastGathered.tm_min < actualTime.tm_min:
        player.info.LastGathered = time.localtime(time.time())
        for wy in range(Map.y_size):
            for wx in range(Map.x_size):
                fort = Map.GetFort(wy, wx)
                if isinstance(fort, Buildings.Fortress) and fort.owner == player:
                    LocalMap.GetProduction(player, wy, wx)  
        Utility.SendMsg(player, Colors.COLOR_GREEN + "All production gathered!\n")   
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Production already gathered!\n") 
        
def ScoutingMode(player):     
    scoutingMenu =  Colors.COLOR_AZURE
    scoutingMenu += "Welcome in Scouting Menu!\n"
    scoutingMenu += "available options are:\n"
    Utility.SendMsg(player, scoutingMenu) 
    Utility.SendMsg(player, Commands.GetCommands(MainCommands)) 
    
    player.state = State.SCOUTING_MODE
    while player.state == State.SCOUTING_MODE:
        Utility.SendMsg(player, Control.CTRL_MENU_SCOUTING_MODE)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        # MainCommands >>>
        if command == MainCommands._0_0_SHOW_MAP:
            LocalMap.ShowMap(player)
        elif command == MainCommands._1_0_SHOW_RESOURCES:
            player.ShowResources()
        elif command == MainCommands._2_0_RETURN:
            Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to World Map!\n")
            player.state = State.WORLD_MAP
        elif command == MainCommands._3_0_EXIT:
            Utility.SendMsg(player, Control.CTRL_EXIT)
            player.state = State.EXITING
        # MainCommands <<<
        elif command == ScoutingCommands._0_0_SHOW_ENEMY_INFO:
            fort = Map.GetFort(player.wy, player.wx)  
            Utility.SendMsg(player, Colors.COLOR_BLOOD + fort.owner.username + " own this fortress!\n")     
        
def AttackFortress(player, wy ,wx):
    if isinstance(Map.GetFort(wy, wx), Buildings.Fortress):
        if Map.GetFort(wy, wx).owner != player:
            player.wy = wy
            player.wx = wx   
            Attack.AttackFortress(player, wy, wx)
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Can't attack own fortress!\n")
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Field is empty!\n")