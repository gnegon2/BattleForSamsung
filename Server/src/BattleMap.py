from Colors import Colors
from Pos import Pos
import Utility
import Log
import Geo
import Map

class BattleMap():
       
    def __init__(self, player, army, wy, wx):
        Log.Save("Init BattleMap!\n")
        self.player = player
        self.army = army
        self.cwy = wy
        self.cwx = wx
        
        self.offset = Map.firstQ
        if self.army[Geo.NORTH]:
            self.nwy = wy - 1
            self.nwx = wx
        if self.army[Geo.SOUTH]:
            self.swy = wy + 1
            self.swx = wx
        if self.army[Geo.EAST]:
            self.ewy = wy
            self.ewx = wx + 1
        if self.army[Geo.WEST]:
            self.wwy = wy
            self.wwx = wx - 1
            self.offset = Map.half
       
    def ShowBattleMap(self):
        if self.army[Geo.NORTH]:
            self.ShowMapSouth()
        self.ShowCentralMap()
        if self.army[Geo.SOUTH]:
            self.ShowMapNorth()
 
    def ShowCentralMap(self):     
        mapMsg = Colors.COLOR_WHITE
        # NORTH
        for y in range(Map.firstQ):
            for x in range(Map.firstQ):
                mapMsg += " "
            if self.army[Geo.WEST]:
                for x in range(Map.thirdQ, Map.end):
                    mapMsg += " "
            for x in range(Map.firstQ, Map.thirdQ):   
                instance = Map.Get(Pos(self.cwy, self.cwx, y, x))
                mapMsg += instance.color + instance.field
            mapMsg += "\n"
        # CENTRAL
        for y in range(Map.firstQ, Map.thirdQ):
            if self.army[Geo.WEST]:
                for x in range(Map.thirdQ, Map.end):   
                    instance = Map.Get(Pos(self.wwy, self.wwx, y, x)) 
                    mapMsg += instance.color + instance.field
            for x in range(Map.end):   
                instance = Map.Get(Pos(self.cwy, self.cwx, y, x))
                mapMsg += instance.color + instance.field
            if self.army[Geo.EAST]:
                for x in range(Map.firstQ):   
                    instance = Map.Get(Pos(self.wwy, self.wwx, y, x))
                    mapMsg += instance.color + instance.field
            mapMsg += "\n"
        # SOUTH
        for y in range(Map.thirdQ, Map.end):
            for x in range(0, Map.firstQ):
                mapMsg += " "
            if self.army[Geo.WEST]:
                for x in range(Map.thirdQ, Map.end):
                    mapMsg += " "
            for x in range(Map.firstQ, Map.thirdQ):   
                instance = Map.Get(Pos(self.cwy, self.cwx, y, x))
                mapMsg += instance.color + instance.field
            mapMsg += "\n"
        Utility.SendMsg(self.player, mapMsg)
             
    def ShowMapNorth(self):  
        mapMsg =  Colors.COLOR_WHITE   
        for y in range(0, Map.firstQ):
            for x in range(0, self.offset):
                mapMsg += " "
            for x in range(Map.firstQ, Map.thirdQ):
                instance = Map.Get(Pos(self.swy, self.swx, y, x))
                mapMsg += instance.color + instance.field
            mapMsg += "\n"
        Utility.SendMsg(self.player, mapMsg)
          
    def ShowMapSouth(self):  
        mapMsg =  Colors.COLOR_WHITE   
        for y in range(Map.thirdQ, Map.end):
            for x in range(self.offset):
                mapMsg += " "
            for x in range(Map.firstQ, Map.thirdQ):
                instance = Map.Get(Pos(self.nwy, self.nwx, y, x))
                mapMsg += instance.color + instance.field
            mapMsg += "\n"
        Utility.SendMsg(self.player, mapMsg)