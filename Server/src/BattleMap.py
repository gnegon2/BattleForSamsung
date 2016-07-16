from LocalMapStruct import localMaps
import Control
import Utility
import Log
import Config

class BattleMap():
       
    def __init__(self, player, army, y, x):
        Log.Save("Init BattleMap!\n")
        self.player = player
        self.army = army
        self.y = y
        self.x = x
        
        self.offset = 5
        if self.army['OnWest']:
            self.offset = 10
       
    def ShowBattleMap(self):
        if self.army['OnNorth']:
            self.ShowMapSouth()
        self.ShowCentralMap()
        if self.army['OnSouth']:
            self.ShowMapNorth()
 
    def ShowCentralMap(self):     
        localMapStructCentral = localMaps[self.player.localMapY][self.player.localMapX]
        localMapStructWest = localMaps[self.player.localMapY][self.player.localMapX-1]
        localMapStructEast = localMaps[self.player.localMapY][self.player.localMapX+1]
        mapMsg = Control.CTRL_COLOR_WHITE
        # NORTH
        for y in range(0, Config.localMapSize/4):
            for x in range(0, Config.localMapSize/4):
                mapMsg += " "
            if self.army['OnWest']:
                for x in range(3*Config.localMapSize/4, Config.localMapSize):
                    mapMsg += " "
            for x in range(Config.localMapSize/4, 3*Config.localMapSize/4):   
                instance = localMapStructCentral.fields[y][x]
                mapMsg += instance.color + instance.field
            mapMsg += "\n"
        # CENTRAL
        for y in range(Config.localMapSize/4, 3*Config.localMapSize/4):
            if self.army['OnWest']:
                for x in range(3*Config.localMapSize/4, Config.localMapSize):   
                    instance = localMapStructWest.fields[y][x]
                    mapMsg += instance.color + instance.field
            for x in range(0, Config.localMapSize):   
                instance = localMapStructCentral.fields[y][x]
                mapMsg += instance.color + instance.field
            if self.army['OnEast']:
                for x in range(0, Config.localMapSize/4):   
                    instance = localMapStructEast.fields[y][x]
                    mapMsg += instance.color + instance.field
            mapMsg += "\n"
        # SOUTH
        for y in range(3*Config.localMapSize/4, Config.localMapSize):
            for x in range(0, Config.localMapSize/4):
                mapMsg += " "
            if self.army['OnWest']:
                for x in range(3*Config.localMapSize/4, Config.localMapSize):
                    mapMsg += " "
            for x in range(Config.localMapSize/4, 3*Config.localMapSize/4):   
                instance = localMapStructCentral.fields[y][x]
                mapMsg += instance.color + instance.field
            mapMsg += "\n"
        Utility.SendMsg(self.player, mapMsg)
             
    def ShowMapNorth(self):  
        mapMsg =  Control.CTRL_COLOR_WHITE   
        localMapStruct = localMaps[self.y+1][self.x]
        for y in range(0, Config.localMapSize / 4):
            for x in range(0, self.offset):
                mapMsg += " "
            for x in range(Config.localMapSize / 4, 3 * Config.localMapSize / 4):
                instance = localMapStruct.fields[y][x]
                mapMsg += instance.color + instance.field
            mapMsg += "\n"
        Utility.SendMsg(self.player, mapMsg)
          
    def ShowMapSouth(self):  
        mapMsg =  Control.CTRL_COLOR_WHITE   
        localMapStruct = localMaps[self.y-1][self.x]
        for y in range(3 * Config.localMapSize / 4, Config.localMapSize):
            for x in range(0, self.offset):
                mapMsg += " "
            for x in range(Config.localMapSize / 4, 3 * Config.localMapSize / 4):
                instance = localMapStruct.fields[y][x]
                mapMsg += instance.color + instance.field
            mapMsg += "\n"
        Utility.SendMsg(self.player, mapMsg)