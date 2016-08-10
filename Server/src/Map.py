from Database import Database
from Pos import Pos
import Config
import Buildings
import weakref

class Map():    
    firstQ = Config.localMapSize/4
    half = Config.localMapSize/2
    thirdQ = 3*Config.localMapSize/4
    end =  Config.localMapSize
    
    def __init__(self):
        self.y_size = 0
        self.x_size = 0
        self.fields = []
        
    def Load(self, obj):
        self.y_size = obj.y_size
        self.x_size = obj.x_size
        self.fields = obj.fields

    def GetFort(self, wy, wx):
        fort = self.Get(Pos(wy, wx, self.half-1, self.half-1))
        if isinstance(fort, Buildings.Fortress):
            return fort
        fort = self.Get(Pos(wy, wx, self.half, self.half-1))
        if isinstance(fort, Buildings.Fortress):
            return fort
        fort = self.Get(Pos(wy, wx, self.half-1, self.half))
        if isinstance(fort, Buildings.Fortress):
            return fort
        fort = self.Get(Pos(wy, wx, self.half, self.half))
        if isinstance(fort, Buildings.Fortress):
            return fort
        return None
    
    def SetFort(self, player, wy, wx):
        self.Set(player, Buildings.Fortress, Pos(wy, wx, self.half - 1, self.half - 1))
        self.Set(player, Buildings.Fortress, Pos(wy, wx, self.half - 1, self.half))
        self.Set(player, Buildings.Fortress, Pos(wy, wx, self.half, self.half - 1))
        self.Set(player, Buildings.Fortress, Pos(wy, wx, self.half, self.half))
        Database.SaveDatabase()
        
    def ChangeFortLevel(self, wy, wx, next_level):
        fort = self.Get(Pos(wy, wx, self.half-1, self.half-1))
        self.UpgradeFortress(fort, next_level) 
        fort = self.Get(Pos(wy, wx, self.half, self.half-1))
        self.UpgradeFortress(fort, next_level)
        fort = self.Get(Pos(wy, wx, self.half-1, self.half))
        self.UpgradeFortress(fort, next_level)
        fort = self.Get(Pos(wy, wx, self.half, self.half))
        self.UpgradeFortress(fort, next_level)
        Database.SaveDatabase()
            
    def UpgradeFortress(self, fort, next_level):
        if isinstance(fort, Buildings.Fortress):
            fort.level = next_level
            production = Buildings.Fortress.production_per_level[next_level]
            for resType, resAmount in production.iteritems():
                if resAmount > 0:
                    fort.production[resType] = resAmount
            statistics = Buildings.Fortress.statistics_per_level[next_level]
            for statType, statAmount in statistics.iteritems():
                if statAmount > 0:
                    fort.statistics[statType] = statAmount
        
    def Get(self, pos):
        return weakref.proxy(mainMap.fields[pos.wy*self.end+pos.y][pos.wx*self.end+pos.x])
    
    def SetEmpty(self, pos, save=False):
        mainMap.fields[pos.wy*self.end+pos.y][pos.wx*self.end+pos.x] = Buildings.Empty()
        if save:
            Database.SaveDatabase()
    
    def SetForbidden(self, pos):
        mainMap.fields[pos.wy*self.end+pos.y][pos.wx*self.end+pos.x] = Buildings.Forbidden()
    
    def Set(self, player, instance, pos, save=False):
        mainMap.fields[pos.wy*self.end+pos.y][pos.wx*self.end+pos.x] = instance(player)
        if save:
            Database.SaveDatabase()
        
    def Swap(self, pos1, pos2, save=False):
        field = mainMap.fields[pos2.wy*self.end+pos2.y][pos2.wx*self.end+pos2.x]
        mainMap.fields[pos2.wy*self.end+pos2.y][pos2.wx*self.end+pos2.x] = mainMap.fields[pos1.wy*self.end+pos1.y][pos1.wx*self.end+pos1.x]
        mainMap.fields[pos1.wy*self.end+pos1.y][pos1.wx*self.end+pos1.x] = field
        if save:
            Database.SaveDatabase()

mainMap = Map()

