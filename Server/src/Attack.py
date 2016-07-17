from Colors import Colors
from Battle import Battle
from Pos import Pos
import Log
import Utility
import Units
import Attack
import Geo
import Map

def AttackFortress(player, wy, wx):
    Log.Save(player.username + " attack fortress on field: " + str(wy) + " " + str(wx) + "\n")
    
    fortress = Attack.CheckNearFortress(player, wy, wx)
    
    if any(geo for geo in fortress):
        army = {}
        army[Geo.NORTH] = army[Geo.SOUTH] = army[Geo.EAST] = army[Geo.WEST] = False
        if fortress[Geo.NORTH]:
            army[Geo.NORTH] = Attack.CheckArmy(player, wy-1, wx, Geo.SOUTH)
        if fortress[Geo.SOUTH]:
            army[Geo.SOUTH] = Attack.CheckArmy(player, wy+1, wx, Geo.NORTH)
        if fortress[Geo.EAST]:
            army[Geo.EAST] = Attack.CheckArmy(player, wy, wx+1, Geo.WEST)
        if fortress[Geo.WEST]:
            army[Geo.WEST] = Attack.CheckArmy(player, wy, wx-1, Geo.EAST)
        if any(geo for geo in army):
            Log.Save("Army near fortress!\n")
            battle = Battle(player, army, wy, wx)
            if battle.Start():
                Log.Save(player.username + " destroy enemy fortress!\n")
                Utility.SendMsg(player, Colors.COLOR_GREEN + "Victory!\nReturning to World Map!\n")
                fort = Map.GetFort(wy, wx)
                fort.owner = player
            else:
                Log.Save(player.username + " losses the battle!\n")
                Utility.SendMsg(player, Colors.COLOR_RED + "Lose!\nReturning to World Map!\n")
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "You have no army near attacking fortress!\n")
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "You have no fortress near attacking fortress!\n")

def CheckNearFortress(player, wy, wx):
    fortress = {}
    fortress[Geo.NORTH] = fortress[Geo.SOUTH] = fortress[Geo.EAST] = fortress[Geo.WEST] = False
    fort = Map.GetFort(wy - 1, wx)
    if hasattr(fort, 'owner') and fort.owner == player:
        fortress[Geo.NORTH] = True;
    fort = Map.GetFort(wy + 1, wx)
    if hasattr(fort, 'owner') and fort.owner == player:
        fortress[Geo.SOUTH] = True;
    fort = Map.GetFort(wy, wx + 1)
    if hasattr(fort, 'owner') and fort.owner == player:
        fortress[Geo.EAST] = True;
    fort = Map.GetFort(wy, wx - 1)
    if hasattr(fort, 'owner') and fort.owner == player:
        fortress[Geo.WEST] = True;
    return fortress

def CheckArmy(player, wy, wx, segment):
    if segment == Geo.NORTH:
        startX = Map.firstQ
        stopX = Map.thirdQ
        startY = 0
        stopY = Map.firstQ
    elif segment == Geo.SOUTH:
        startX = Map.firstQ
        stopX = Map.thirdQ
        startY = Map.thirdQ
        stopY = Map.end
    elif segment == Geo.EAST:
        startX = Map.thirdQ
        stopX = Map.end
        startY = Map.firstQ
        stopY = Map.thirdQ
    elif segment == Geo.WEST:
        startX = 0
        stopX = Map.firstQ
        startY = Map.firstQ
        stopY = Map.thirdQ
    for y in range(startY, stopY):
        for x in range(startX, stopX):
            if isinstance(Map.Get(Pos(wy, wx, y, x)), Units.Unit):
                return True
    return False