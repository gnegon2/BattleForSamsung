from Pos import Pos
import Config
import Buildings
import weakref

y_size = 0
x_size = 0
fields = []

firstQ = Config.localMapSize/4
half = Config.localMapSize/2
thirdQ = 3*Config.localMapSize/4
end =  Config.localMapSize

def GetFort(wy, wx):
    pos = Pos(wy, wx, half, half)
    return Get(pos)

def SetFort(player, wy, wx):
    Set(player, Buildings.Fortress, Pos(wy, wx, half - 1, half - 1))
    Set(player, Buildings.Fortress, Pos(wy, wx, half - 1, half))
    Set(player, Buildings.Fortress, Pos(wy, wx, half, half - 1))
    Set(player, Buildings.Fortress, Pos(wy, wx, half, half))

def Get(pos):
    return weakref.proxy(fields[pos.wy*end+pos.y][pos.wx*end+pos.x])

def SetEmpty(pos):
    fields[pos.wy*end+pos.y][pos.wx*end+pos.x] = Buildings.Empty()

def SetForbidden(pos):
    fields[pos.wy*end+pos.y][pos.wx*end+pos.x] = Buildings.Forbidden()

def Set(player, instance, pos):
    fields[pos.wy*end+pos.y][pos.wx*end+pos.x] = instance(player)
    
def Swap(pos1, pos2):
    field = fields[pos2.wy*end+pos2.y][pos2.wx*end+pos2.x]
    fields[pos2.wy*end+pos2.y][pos2.wx*end+pos2.x] = fields[pos1.wy*end+pos1.y][pos1.wx*end+pos1.x]
    fields[pos1.wy*end+pos1.y][pos1.wx*end+pos1.x] = field