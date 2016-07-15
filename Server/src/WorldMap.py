import Config
import re
import time
from LocalMap import LocalMap
from LocalMapStruct import LocalMapStruct
from LocalMapStruct import localMaps
from Commands import WorldMapCommands
from Commands import MainCommands
from WorldMapStruct import WorldMapStruct
from Buildings import Buildings
from Utility import Utility
from Player import State
from Control import Control
from Log import Log
from copy import copy
from Attack import Attack

class Fields:
    EMPTY_FIELD = "0"
    PLAYER_FIELD = "X"

class WorldMap: 
    @staticmethod
    def LoadMap():
        Log.Save("LoadMap.\n")
        inputFile = open(Config.mapPath, 'r')
        data = inputFile.read()
        row = []
        for field in data:
            if field == "\n":
                WorldMapStruct.fields.append(copy(row))
                del row[:]
            elif field != "\r":
                row.append(field)
        WorldMapStruct.fields.append(copy(row))
        WorldMapStruct.sizeY = len(WorldMapStruct.fields)
        WorldMapStruct.sizeX = len(WorldMapStruct.fields[0])
        
    @staticmethod
    def InitLocalMaps():
        Log.Save("InitLocalMaps.\n")
        for worldPosY in range(WorldMapStruct.sizeY):
            worldRow = []; worldPosY
            for worldPosX in range(WorldMapStruct.sizeX):
                localMapStruct = LocalMapStruct(); worldPosX
                for y in range(Config.localMapSize):
                    row = []; y
                    for x in range(Config.localMapSize):
                        row.append(Buildings.Empty()); x
                    localMapStruct.fields.append(copy(row))
                    del row[:]
                localMapStruct.worldPosX = worldPosX
                localMapStruct.worldPosY = worldPosY
                worldRow.append(copy(localMapStruct))
            localMaps.append(copy(worldRow))
            del worldRow[:]                        
            
    @staticmethod
    def InitForbiddenPlaces():
        Log.Save("InitForbiddenPlaces.\n")
        for worldPosY in range(WorldMapStruct.sizeY):
            for worldPosX in range(WorldMapStruct.sizeX):
                localMapStruct = localMaps[worldPosY][worldPosX]
                for y in range(Config.localMapSize/4):
                    for x in range(Config.localMapSize/4):
                        localMapStruct.fields[y][x] = Buildings.Forbidden()
                for y in range(Config.localMapSize/4):
                    for x in range(3*Config.localMapSize/4, Config.localMapSize):
                        localMapStruct.fields[y][x] = Buildings.Forbidden()
                for y in range(3*Config.localMapSize/4, Config.localMapSize):
                    for x in range(Config.localMapSize/4):
                        localMapStruct.fields[y][x] = Buildings.Forbidden()
                for y in range(3*Config.localMapSize/4, Config.localMapSize):
                    for x in range(3*Config.localMapSize/4, Config.localMapSize):
                        localMapStruct.fields[y][x] = Buildings.Forbidden()
    
    @staticmethod
    def ParseCommand(player, command):
        try:
            y, x = map(int, re.findall(r'\d+', command))
            if 0 <= x < WorldMapStruct.sizeX and 0 <= y < WorldMapStruct.sizeY: 
                return True, y, x
            else:
                if not 0 <= x < WorldMapStruct.sizeX:
                    Utility.SendMsg(player, Control.CTRL_COLOR_RED + \
                                    "Value X out of range! X must be in range: 0 - " + str(WorldMapStruct.sizeX-1) + "\n")
                    return False, 0, 0
                if not 0 <= y < WorldMapStruct.sizeY:
                    Utility.SendMsg(player, Control.CTRL_COLOR_RED + \
                                    "Value Y out of range! Y must be in range: 0 - " + str(WorldMapStruct.sizeY-1) + "\n")
                    return False, 0, 0   
        except ValueError:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + \
                            "Bad number of arguments! Provide exactly two arguments!\n")  
            return False, 0, 0   
        
    @staticmethod
    def ExecuteCommand(player, command):
        # MainCommands >>>
        if command == MainCommands.SHOW_MAP:
            WorldMap.ShowMap(player)
        elif command == MainCommands.SHOW_RESOURCES:
            player.ShowResources()
        elif command == MainCommands.RETURN:
            Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Returning to Main Menu!\n")
            player.state = State.INIT
            player.loggedIn = False
        elif command == MainCommands.EXIT:
            Utility.SendMsg(player, Control.CTRL_EXIT)
            player.state = State.EXITING
        # MainCommands <<<     
        elif command == WorldMapCommands.GET_PRODUCTION:
            WorldMap.GetProduction(player)
        elif command == WorldMapCommands.SHOW_FORTRESS_INFO:
            Buildings.ShowInfo(player, Buildings.Fortress(player))
        elif command.find(WorldMapCommands.SETTLE_FORTRESS) == 0 or \
             command.find(WorldMapCommands.ENTER_FORTRESS) == 0:
            succes, y, x = WorldMap.ParseCommand(player, command)
            if succes:
                if command.find(WorldMapCommands.SETTLE_FORTRESS) == 0:
                    WorldMap.SettleFortress(player, y, x)
                elif command.find(WorldMapCommands.ENTER_FORTRESS) == 0:
                    WorldMap.EnterFortress(player, y, x)
        elif command.find(WorldMapCommands.ATTACK_FORTRESS) == 0:
            succes, y, x = WorldMap.ParseCommand(player, command)
            if succes:
                WorldMap.AttackFortress(player, y, x)
        else:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Undefined command! Try again!\n")
    
    
    @staticmethod    
    def ShowMap(player):
        mapMsg = Control.CTRL_COLOR_WHITE
        row, col = 0, 0
        mapMsg += "  "
        for x in range(0, WorldMapStruct.sizeX):
            if col < 10:
                mapMsg += " "
            mapMsg += str(col)
            mapMsg += " "
            col += 1
        mapMsg += "\n"
        for y in range(0, WorldMapStruct.sizeY):
            if row < 10:
                mapMsg += " "
            mapMsg += str(row)
            row += 1
            for x in range(0, WorldMapStruct.sizeX):  
                field = WorldMapStruct.fields[y][x]
                mapMsg += " "
                if field == Fields.EMPTY_FIELD:
                    mapMsg += Control.CTRL_COLOR_BROWN + field
                elif field == player.username:
                    mapMsg += Control.CTRL_COLOR_GREEN + Fields.PLAYER_FIELD
                else:
                    mapMsg += Control.CTRL_COLOR_RED + Fields.PLAYER_FIELD
                mapMsg += Control.CTRL_COLOR_WHITE + " "
            mapMsg += "\n\n"    
        Utility.SendMsg(player, mapMsg)   
    
    @staticmethod
    def SettleFortress(player, y, x):
        if WorldMapStruct.fields[y][x] == Fields.EMPTY_FIELD:
            if Buildings.Build(player, Buildings.Fortress(player)):
                Log.Save(player.username + " construct new fortress on " + str(y) + " " + str(x) + "!\n")
                WorldMapStruct.fields[y][x] = player.username
                LocalMap.InitMap(player, y, x)
                Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Fortress successfully settled!\n") 
            else:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Not enough resources!\n") 
        else:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Field is not empty!\n")
            
    @staticmethod
    def EnterFortress(player, y, x):
        if WorldMapStruct.fields[y][x] != Fields.EMPTY_FIELD:
            player.localMapX = x
            player.localMapY = y
            if WorldMapStruct.fields[y][x] == player.username:
                player.state = State.LOCAL_MAP
            else:
                WorldMap.ScoutingMode(player)
        else:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Field is empty!\n")
            
    @staticmethod
    def GetProduction(player):
        actualTime = time.localtime(time.time())
        if player.info.LastGathered.tm_year < actualTime.tm_year or \
            player.info.LastGathered.tm_mon < actualTime.tm_mon or \
            player.info.LastGathered.tm_mday < actualTime.tm_mday or \
            player.info.LastGathered.tm_min < actualTime.tm_min:
            player.info.LastGathered = time.localtime(time.time())
            for y in range(0, WorldMapStruct.sizeY):
                for x in range(0, WorldMapStruct.sizeX): 
                    if WorldMapStruct.fields[y][x] == player.username:
                        LocalMap.GetProduction(player, y, x)  
            Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "All production gathered!\n")   
        else:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Production already gathered!\n") 
            
    @staticmethod
    def ScoutingMode(player):     
        scoutingMenu =  Control.CTRL_COLOR_AZURE
        scoutingMenu += "Welcome in Scouting Menu!\n"
        scoutingMenu += "available options are:\n"
        Utility.SendMsg(player, scoutingMenu)
        Utility.SendMsg(player, MainCommands.Get())   
        
        player.state = State.SCOUTING_MODE
        while player.state == State.SCOUTING_MODE:
            Utility.SendMsg(player, Control.CTRL_SCOUTING_MODE)
            command = Utility.SendMsg(player, Control.CTRL_INPUT)
            # MainCommands >>>
            if command == MainCommands.SHOW_MAP:
                LocalMap.ShowMap(player)
            elif command == MainCommands.SHOW_RESOURCES:
                player.ShowResources()
            elif command == MainCommands.RETURN:
                Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Returning to World Map!\n")
                player.state = State.WORLD_MAP
            elif command == MainCommands.EXIT:
                Utility.SendMsg(player, Control.CTRL_EXIT)
                player.state = State.EXITING
            # MainCommands <<<        
            
    @staticmethod
    def AttackFortress(player, y ,x):
        if WorldMapStruct.fields[y][x] != Fields.EMPTY_FIELD:
            if WorldMapStruct.fields[y][x] == player.username:
                player.localMapX = x
                player.localMapY = y    
                Attack.AttackFortress(player, y, x)
            else:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Can't attack own fortress!\n")
        else:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Field is empty!\n")