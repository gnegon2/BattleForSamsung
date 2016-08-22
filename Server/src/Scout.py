from Commands import ScoutingCommands
from Commands import MainCommands
from Resources import Resources
from Map import mainMap as Map
from Colors import Colors
from Pos import Pos
import Utility
import Commands
import State
import Control
from Database import Database

class Cost():
    entire_cost = Resources()
    entire_cost.Init(500)

    rest_cost = Resources()
    rest_cost.Init(100)

def ShowCost():
    msg = Colors.COLOR_GREEN
    msg += "Scout entire map cost is: \n" 
    for resType, resAmount in Cost.entire_cost.iteritems():
        if resAmount > 0:
            msg += resType.color + resType.name + ": " + str(resAmount) + "\n"
    msg += Colors.COLOR_GREEN + "Scout north/south/east/west map cost is: \n" 
    for resType, resAmount in Cost.rest_cost.iteritems():
        if resAmount > 0:
            msg += resType.color + resType.name + ": " + str(resAmount) + "\n"
    return msg

def ShowFogMap(player):     
    row, col = 0, 0
    mapMsg = Colors.COLOR_WHITE + "  "
    for _ in range(Map.end):
        if col < 10:
            mapMsg += " "
        mapMsg += Colors.COLOR_WHITE + str(col)
        mapMsg += " "
        col += 1
    mapMsg += "\n"
    for _ in range(Map.end):
        if row < 10:
            mapMsg += " "
        mapMsg += Colors.COLOR_WHITE + str(row)
        row += 1
        for _ in range(0, Map.end): 
            mapMsg += " "
            mapMsg += "X"
            mapMsg += " "
        mapMsg += "\n\n"
    Utility.SendMsg(player, mapMsg)

def ShowEntireMap(player):     
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
    
def ShowNorth(player):     
    row, col = 0, 0
    mapMsg = Colors.COLOR_WHITE + "  "
    for x in range(Map.end):
        if col < 10:
            mapMsg += " "
        mapMsg += Colors.COLOR_WHITE + str(col)
        mapMsg += " "
        col += 1
    mapMsg += "\n"
    for y in range(Map.firstQ):
        if row < 10:
            mapMsg += " "
        mapMsg += Colors.COLOR_WHITE + str(row)
        row += 1
        for x in range(Map.end): 
            instance = Map.Get(Pos(player.wy, player.wx, y, x))
            mapMsg += " "
            mapMsg += instance.color + instance.field
            mapMsg += " "
        mapMsg += "\n\n"
    for y in range(Map.firstQ, Map.end):
        if row < 10:
            mapMsg += " "
        mapMsg += Colors.COLOR_WHITE + str(row)
        row += 1
        for x in range(Map.end): 
            mapMsg += " "
            mapMsg += "X"
            mapMsg += " "
        mapMsg += "\n\n"
    Utility.SendMsg(player, mapMsg)
    
def ShowSouth(player):     
    row, col = 0, 0
    mapMsg = Colors.COLOR_WHITE + "  "
    for x in range(Map.end):
        if col < 10:
            mapMsg += " "
        mapMsg += Colors.COLOR_WHITE + str(col)
        mapMsg += " "
        col += 1
    mapMsg += "\n"
    for y in range(Map.thirdQ):
        if row < 10:
            mapMsg += " "
        mapMsg += Colors.COLOR_WHITE + str(row)
        row += 1
        for _ in range(Map.end): 
            mapMsg += " "
            mapMsg += "X"
            mapMsg += " "
        mapMsg += "\n\n"
    for y in range(Map.thirdQ, Map.end):
        if row < 10:
            mapMsg += " "
        mapMsg += Colors.COLOR_WHITE + str(row)
        row += 1
        for x in range(Map.end): 
            instance = Map.Get(Pos(player.wy, player.wx, y, x))
            mapMsg += " "
            mapMsg += instance.color + instance.field
            mapMsg += " "
        mapMsg += "\n\n"
    Utility.SendMsg(player, mapMsg)
    
def ShowEast(player):     
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
        for _ in range(Map.thirdQ): 
            mapMsg += " "
            mapMsg += "X"
            mapMsg += " "
        for x in range(Map.thirdQ, Map.end): 
            instance = Map.Get(Pos(player.wy, player.wx, y, x))
            mapMsg += " "
            mapMsg += instance.color + instance.field
            mapMsg += " "
        mapMsg += "\n\n"
    Utility.SendMsg(player, mapMsg)
    
def ShowWest(player):     
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
        for x in range(Map.firstQ): 
            instance = Map.Get(Pos(player.wy, player.wx, y, x))
            mapMsg += " "
            mapMsg += instance.color + instance.field
            mapMsg += " "
        for _ in range(Map.firstQ, Map.end): 
            mapMsg += " "
            mapMsg += "X"
            mapMsg += " "
        mapMsg += "\n\n"
    Utility.SendMsg(player, mapMsg)
    
def ScoutingMode(player):     
    scoutingMenu =  Colors.COLOR_AZURE
    scoutingMenu += "Welcome in Scouting Menu!\n"
    scoutingMenu += "available options are:\n"
    Utility.SendMsg(player, scoutingMenu) 
    Utility.SendMsg(player, Commands.GetCommands(ScoutingCommands)) 
    Utility.SendMsg(player, Commands.GetCommands(MainCommands)) 
    
    player.state = State.SCOUTING_MODE
    while player.state == State.SCOUTING_MODE:
        Utility.SendMsg(player, Control.CTRL_MENU_SCOUTING_MODE)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        # MainCommands >>>
        if command == MainCommands._0_0_SHOW_MAP:
            ShowFogMap(player)
        elif command == MainCommands._1_0_SHOW_RESOURCES:
            player.ShowResources()
        elif command == MainCommands._3_0_RETURN:
            Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to World Map!\n")
            player.state = State.WORLD_MAP
            Database.SaveDatabase()
        elif command == MainCommands._4_0_EXIT:
            Utility.SendMsg(player, Control.CTRL_EXIT)
            player.state = State.EXITING
            Database.SaveDatabase()
        # MainCommands <<<
        elif command == ScoutingCommands._0_0_SHOW_INFO:
            fort = Map.GetFort(player.wy, player.wx)  
            Utility.SendMsg(player, Colors.COLOR_BLOOD + fort.owner + " own this fortress!\n")
            Utility.SendMsg(player, ShowCost())
        elif command == ScoutingCommands._1_0_SCOUT_ENTIRE_MAP:
            if player.Pay(Cost.entire_cost, 100):
                ShowEntireMap(player)
        elif command == ScoutingCommands._2_0_SCOUT_NORTH_MAP:
            if player.Pay(Cost.rest_cost, 100):
                ShowNorth(player)
        elif command == ScoutingCommands._3_0_SCOUT_SOUTH_MAP:
            if player.Pay(Cost.rest_cost, 100):
                ShowSouth(player)        
        elif command == ScoutingCommands._4_0_SCOUT_EAST_MAP:
            if player.Pay(Cost.rest_cost, 100):
                ShowEast(player)       
        elif command == ScoutingCommands._5_0_SCOUT_WEST_MAP:
            if player.Pay(Cost.rest_cost, 100):
                ShowWest(player)
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Undefined command! Try again!\n")      