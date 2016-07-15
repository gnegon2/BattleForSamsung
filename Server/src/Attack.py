from Log import Log
from LocalMapStruct import localMaps
from Utility import Utility
from Control import Control, Type
from WorldMapStruct import WorldMapStruct
from Battle import Battle
import Config

class Attack():
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"
    
    @staticmethod
    def AttackFortress(player, y, x):
        Log.Save(player.username + " attack fortress on field: " + str(y) + " " + str(x) + "\n")
        
        fortress = Attack.CheckNearFortress(player, y, x)
        
        if fortress['Any']:
            army = {}
            army['OnNorth'] = False
            army['OnSouth'] = False
            army['OnEast'] = False
            army['OnWest'] = False
            if fortress['OnNorth']:
                army['OnNorth'] = Attack.CheckArmy(player, y-1, x, Attack.SOUTH)
            if fortress['OnSouth']:
                army['OnSouth'] = Attack.CheckArmy(player, y+1, x, Attack.NORTH)
            if fortress['OnEast']:
                army['OnEast'] = Attack.CheckArmy(player, y, x+1, Attack.WEST)
            if fortress['OnWest']:
                army['OnWest'] = Attack.CheckArmy(player, y, x-1, Attack.EAST)
            if army['OnNorth'] or army['OnSouth'] or army['OnEast'] or army['OnWest']:
                Log.Save("Army near fortress!\n")
                battle = Battle(player, WorldMapStruct.fields[y][x], army, y, x)
                battle.Start()
            else:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You have no army near attacking fortress!\n")
        else:
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You have no fortress near attacking fortress!\n")
    
    @staticmethod
    def CheckNearFortress(player, y, x):
        fortress = {}
        fortress['Any'] = False
        fortress['OnNorth'] = False
        fortress['OnSouth'] = False
        fortress['OnEast'] = False
        fortress['OnWest'] = False
        if WorldMapStruct.fields[y-1][x] == player.username:
            fortress['OnNorth'] = True; fortress['Any'] = True
        if WorldMapStruct.fields[y+1][x] == player.username:
            fortress['OnSouth'] = True; fortress['Any'] = True
        if WorldMapStruct.fields[y][x+1] == player.username:
            fortress['OnEast'] = True; fortress['Any'] = True
        if WorldMapStruct.fields[y][x-1] == player.username:
            fortress['OnWest'] = True; fortress['Any'] = True
        return fortress
    
    @staticmethod
    def CheckArmy(player, y, x, segment):
        if segment == Attack.NORTH:
            startX = Config.localMapSize/4
            stopX = 3*Config.localMapSize/4
            startY = 0
            stopY = Config.localMapSize/4
        elif segment == Attack.SOUTH:
            startX = Config.localMapSize/4
            stopX = 3*Config.localMapSize/4
            startY = 3*Config.localMapSize/4
            stopY = Config.localMapSize
        elif segment == Attack.EAST:
            startX = 3*Config.localMapSize/4
            stopX = Config.localMapSize
            startY = Config.localMapSize/4
            stopY = 3*Config.localMapSize/4
        elif segment == Attack.WEST:
            startX = 0
            stopX = Config.localMapSize/4
            startY = Config.localMapSize/4
            stopY = 3*Config.localMapSize/4
        localMapStruct = localMaps[y][x]
        for y_arg in range(startY, stopY):
            for x_arg in range(startX, stopX):
                if localMapStruct.fields[y_arg][x_arg].type == Type.UNIT:
                    return True
        return False