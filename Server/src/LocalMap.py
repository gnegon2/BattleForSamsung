from Colors import Colors
import Commands
from Commands import MainCommands, BuildingCommands
from Commands import LocalMapCommands
from Commands import ActionCommands
from Commands import UnitsCommands
from Resources import Resources
from Map import mainMap as Map
from Pos import Pos
import Log
import Buildings
import Units
import Utility
import Control
import State
import Config
import re
import Statistics
import Geo
from Buildings import Fortress
 
def ParseCommandXY(player, command):
    try:
        y, x = map(int, re.findall(r'\d+', command))
        if 0 <= x < Map.end and 0 <= y < Map.end:
            return True, y, x
        else:
            if not 0 <= x < Map.end:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value X out of range! X must be in range: 0 - " + str(Map.end - 1) + "\n")
                return False, 0, 0
            if not 0 <= y < Map.end:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value Y out of range! Y must be in range: 0 - " + str(Map.end - 1) + "\n")
                return False, 0, 0
    except ValueError:
        Utility.SendMsg(player, Colors.COLOR_RED + "Bad number of arguments! Provide exactly two arguments!\n")
        return False, 0, 0
 
def ExecuteCommand(player, command):
    # MainCommands >>>
    if command == MainCommands._0_0_SHOW_MAP:
        ShowMap(player)
    elif command == MainCommands._1_0_SHOW_RESOURCES:
        player.ShowResources()
    elif command == MainCommands._2_0_RETURN:
        Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to World Map!\n")
        player.state = State.WORLD_MAP
    elif command == MainCommands._3_0_EXIT:
        Utility.SendMsg(player, Control.CTRL_EXIT)
        player.state = State.EXITING
    # MainCommands <<<   
    elif command == LocalMapCommands._0_0_BUILDINGS:
        BuildingMenu(player)
    elif command == LocalMapCommands._1_0_ARMY:
        UnitsMenu(player)
    elif command.find(LocalMapCommands._2_2_DESTROY) != -1 or \
         command.find(LocalMapCommands._3_2_REPAIR) != -1 or \
         command.find(LocalMapCommands._4_2_SHOW_DETAIL_INFO) != -1:
        succes, y, x = ParseCommandXY(player, command)
        if succes:
            if command.find(LocalMapCommands._2_2_DESTROY) != -1:
                Destroy(player, y, x)
            elif command.find(LocalMapCommands._3_2_REPAIR) != -1:
                if not Repair(player, y, x):
                    Utility.SendMsg(player, Colors.COLOR_RED + "Nothing to repair!\n")
            elif command.find(LocalMapCommands._4_2_SHOW_DETAIL_INFO) != -1:
                ShowDetailInfo(player, y, x)
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Undefined command!\n")
   
def ShowMap(player):     
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
        for x in range(Map.end):   
            instance = Map.Get(Pos(player.wy, player.wx, y, x))
            mapMsg += " "
            mapMsg += instance.color + instance.field
            mapMsg += " "
        mapMsg += "\n\n"
    Utility.SendMsg(player, mapMsg)

def BuildingMenu(player):
    Log.Save(player.username + " enters Building Menu\n")
    buildingMenu = Colors.COLOR_AZURE
    buildingMenu += "Welcome in Building Menu!\n"
    buildingMenu += "available options are:\n"
    Utility.SendMsg(player, buildingMenu)
    Utility.SendMsg(player, Commands.GetCommands(BuildingCommands))
    Utility.SendMsg(player, Commands.GetCommands(MainCommands))
    
    player.state = State.BUILDING_MENU
    while player.state == State.BUILDING_MENU:
        Utility.SendMsg(player, Control.CTRL_MENU_BUILDING)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        Log.Save(player.username + " enter command: " + command + "\n")
        fort = Map.GetFort(player.wy, player.wx) 
        if fort is not None and fort.owner == player.username:
            # MainCommands >>>
            if command == MainCommands._0_0_SHOW_MAP:
                ShowMap(player)
            elif command == MainCommands._1_0_SHOW_RESOURCES:
                player.ShowResources()
            elif command == MainCommands._2_0_RETURN:
                player.state = State.LOCAL_MAP
                Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to Local Map!\n")
            elif command == MainCommands._3_0_EXIT:
                Utility.SendMsg(player, Control.CTRL_EXIT)
                player.state = State.EXITING
            # MainCommands <<<
            elif command == BuildingCommands._8_0_UPGRADE_FORTRESS:
                UpgradeFortress(player)
            else:
                building = Buildings.CommandToBuilding(command)
                if isinstance(building, Buildings.Empty):
                    Utility.SendMsg(player, Colors.COLOR_RED + "Undefined building!\n")
                else:
                    BuildingActionMenu(player, building)
        else:
            player.state = State.WORLD_MAP
            Utility.SendMsg(player, "Fortress overtaken!\n Returning to World Map!\n") 

def BuildingActionMenu(player, building):
    Log.Save(player.username + " enters building action menu\n")
    actionsMenu = Colors.COLOR_AZURE
    actionsMenu += "available actions on buildings are:\n"
    Utility.SendMsg(player, actionsMenu)
    Utility.SendMsg(player, Commands.GetCommands(ActionCommands))
    Utility.SendMsg(player, Commands.GetCommands(MainCommands))
    
    player.state = State.BUILDING_ACTION_MENU
    while player.state == State.BUILDING_ACTION_MENU:
        Utility.SendMsg(player, Control.CTRL_MENU_ACTION)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        Log.Save(player.username + " enter command: " + command + "\n")
        fort = Map.GetFort(player.wy, player.wx) 
        if fort is not None and fort.owner == player.username:
            # MainCommands >>>
            if command == MainCommands._0_0_SHOW_MAP:
                ShowMap(player)
            elif command == MainCommands._1_0_SHOW_RESOURCES:
                player.ShowResources()
            elif command == MainCommands._2_0_RETURN:
                player.state = State.BUILDING_MENU
                Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to Building Menu!\n")
            elif command == MainCommands._3_0_EXIT:
                Utility.SendMsg(player, Control.CTRL_EXIT)
                player.state = State.EXITING
            # MainCommands <<<
            elif command == ActionCommands._0_0_SHOW_INFO:
                    Buildings.ShowInfo(player, building)
            elif command.find(ActionCommands._1_2_CREATE) == 0:
                succes, y, x = ParseCommandXY(player, command)
                if succes:
                    CreateBuilding(player, building, y, x)
            else:
                Utility.SendMsg(player, Colors.COLOR_RED + "Undefined action!\n")
        else:
            player.state = State.WORLD_MAP
            Utility.SendMsg(player, "Fortress overtaken!\n Returning to World Map!\n")

def CreateBuilding(player, building, y, x):
    Log.Save(player.username + " try to create building\n")
    if Map.firstQ <= x < Map.thirdQ and Map.firstQ <= y < Map.thirdQ:
        player.info.CheckLastBuild()
        if player.info.buildingsBuildToday < Config.maxBuildingsPerDay or Config.maxBuildingsPerDay == 0:
            pos = Pos(player.wy, player.wx, y, x)
            field = Map.Get(pos)
            if isinstance(field, Buildings.Empty):
                if player.Pay(building.cost, 100): 
                    Map.Set(player, building, pos)
                    player.info.buildingsBuildToday += 1
                    Utility.SendMsg(player, Colors.COLOR_GREEN + "Building created!\n")
                    Log.Save(player.username + " created building: " + building.__name__ +"\n") 
                else:
                    Utility.SendMsg(player, Colors.COLOR_RED + "Not enough resources!\n") 
            else:
                Utility.SendMsg(player, Colors.COLOR_RED + "Field is not empty!\n") 
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "You have built maximum buildings today!\n")  
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "You can build only in the central area!\n")      
        
def GetProduction(player, wy, wx):
    Log.Save(player.username + " take production on: " + str(wy) + " " + str(wx) + "\n") 
    Utility.SendMsg(player, Colors.COLOR_GREEN + "Fortress on field: " + str(wy) + ", " + str(wx) + " produce:\n")
    resource = Resources()
    resource.Init()
    for y in range(Map.end):
        for x in range(Map.end):
            building = Map.Get(Pos(wy, wx, y, x))
            if isinstance(building, Buildings.Building):
                resource = Buildings.GetProduction(resource, building)
    for iType, iAmount in resource.iteritems():
        if iAmount > 0:
            player.resources[iType] += iAmount
            Utility.SendMsg(player,  iType.color + iType.name + " = " + str(iAmount) + "\n")
            
                                 
def UnitsMenu(player):
    level = Map.GetFort(player.wy, player.wx).level
    Log.Save(player.username + " enters units menu\n")
    unitsMenu = Colors.COLOR_AZURE
    unitsMenu += "Welcome in Units Menu!\n"
    unitsMenu += "available options are:\n"
    Utility.SendMsg(player, unitsMenu)
    Utility.SendMsg(player, Commands.GetUnitCommands(level))
    Utility.SendMsg(player, Commands.GetCommands(MainCommands))
    
    player.state = State.UNITS_MENU
    while player.state == State.UNITS_MENU:
        Utility.SendMsg(player, Control.CTRL_MENU_UNITS + str(level))
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        Log.Save(player.username + " enter command: " + command + "\n")
        fort = Map.GetFort(player.wy, player.wx) 
        if fort is not None and fort.owner == player.username:
            # MainCommands >>>
            if command == MainCommands._0_0_SHOW_MAP:
                ShowMap(player)
            elif command == MainCommands._1_0_SHOW_RESOURCES:
                player.ShowResources()
            elif command == MainCommands._2_0_RETURN:
                player.state = State.LOCAL_MAP
                Utility.SendMsg(player, Control.CTRL_MENU_LOCAL_MAP)
                Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to Local Map!\n")
            elif command == MainCommands._3_0_EXIT:
                Utility.SendMsg(player, Control.CTRL_EXIT)
                player.state = State.EXITING
            # MainCommands <<<
            elif command.find(UnitsCommands._0_4_MOVE_UNIT) != -1:
                succes, y1, x1, y2, x2, = ParseCommandFour(player, command)
                if succes:
                    MoveUnit(player, player.wy, player.wx, y1, x1, y2, x2)
            else:
                unit = Units.CommandToUnit(command)
                if unit is Units.Empty:
                    Utility.SendMsg(player, Colors.COLOR_RED + "Undefined unit!\n")
                else:
                    UnitsActionMenu(player, unit)
        else:
            player.state = State.WORLD_MAP
            Utility.SendMsg(player, "Fortress overtaken!\n Returning to World Map!\n")
                
def UnitsActionMenu(player, unit): 
    Log.Save(player.username + " enters units action menu\n") 
    actionsMenu = Colors.COLOR_AZURE
    actionsMenu += "available actions on units are:\n"
    Utility.SendMsg(player, actionsMenu)  
    Utility.SendMsg(player, Commands.GetCommands(ActionCommands))
    Utility.SendMsg(player, Commands.GetCommands(MainCommands))   
    
    player.state = State.UNITS_ACTION_MENU
    while player.state == State.UNITS_ACTION_MENU:
        Utility.SendMsg(player, Control.CTRL_MENU_ACTION)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        Log.Save(player.username + " enter command: " + command + "\n")
        fort = Map.GetFort(player.wy, player.wx) 
        if fort is not None and fort.owner == player.username:
            # MainCommands >>>
            if command == MainCommands._0_0_SHOW_MAP:
                ShowMap(player)
            elif command == MainCommands._1_0_SHOW_RESOURCES:
                player.ShowResources()
            elif command == MainCommands._2_0_RETURN:
                player.state = State.UNITS_MENU
                Utility.SendMsg(player, Colors.COLOR_GREEN + "Returning to Units Menu!\n")
            elif command == MainCommands._3_0_EXIT:
                Utility.SendMsg(player, Control.CTRL_EXIT)
                player.state = State.EXITING
            # MainCommands <<<
            elif command == ActionCommands._0_0_SHOW_INFO:
                Units.ShowInfo(player, unit)
            elif command.find(ActionCommands._1_2_CREATE) == 0:
                succes, y, x = ParseCommandXY(player, command)
                if succes:
                    RecruitUnit(player, unit, y, x) 
            else:
                Utility.SendMsg(player, Colors.COLOR_RED + "Undefined action!\n")
        else:
            player.state = State.WORLD_MAP
            Utility.SendMsg(player, "Fortress overtaken!\n Returning to World Map!\n")
                
def RecruitUnit(player, unit, y, x):
    Log.Save(player.username + " try to recruit unit\n")
    player.info.CheckLastRecruit()
    if player.info.numberOfUnits <= player.info.maxNumberOfUnits:
        if player.info.unitsRecruitedToday < Config.maxUnitsPerDay or Config.maxUnitsPerDay == 0:
            pos = Pos(player.wy, player.wx, y, x)
            field = Map.Get(pos)
            if isinstance(field, Buildings.Empty):
                if player.Pay(unit.cost, 100):
                    player.info.unitsRecruitedToday += 1
                    Map.Set(player, unit, pos)
                    Utility.SendMsg(player, Colors.COLOR_GREEN + "Unit recruited!\n") 
                    Log.Save(player.username + " recruit unit:" + unit.__name__ +"\n") 
                else:
                    Utility.SendMsg(player, Colors.COLOR_RED + "Not enough resources!\n") 
            else:
                Utility.SendMsg(player, Colors.COLOR_RED + "Field is not empty!\n") 
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "You have recruit maximum units today!\n")   
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "You have recruit maximum units!\nBuild new houses to recruit more!\n")  
        
def Destroy(player, y, x):
    pos = Pos(player.wy, player.wx, y, x)
    field = Map.Get(pos)
    Log.Save(player.username + " destory " + field.__class__.__name__ + " on " + str(y) + " " + str(x))
    if not isinstance(field, Buildings.Fortress):
        if isinstance(field, Buildings.Building) or isinstance(field, Units.Unit):
            ReturnResources(player, field.cost, 50)
            Map.SetEmpty(pos)
            Utility.SendMsg(player, Colors.COLOR_GREEN + "Succesfully destroyed!\n")
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "This field can't be destroyed!\n")
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Fortress can't be destroyed!\n")

def Repair(player, y, x):
    pos = Pos(player.wy, player.wx, y, x)
    entity = Map.Get(pos)
    if isinstance(entity, Units.Unit) or isinstance(entity, Buildings.Building):  
        hp_max = entity.__class__.statistics[Statistics.HitPoints]
        hp_res = entity.statistics[Statistics.HitPoints]
        percent = int((hp_max - hp_res / float(hp_max)) * 100)  
        if percent == 100:
            if player.Pay(entity.cost, percent):
                Utility.SendMsg(player, Colors.COLOR_GREEN + entity.__class__.__name__ + " succesfully repaired!\n")
                return True
            else:
                Utility.SendMsg(player, Colors.COLOR_RED + "Not enough resources!\n")
                return True
    return False

def RepairFortress(player, wy, wx):
    repaired = False
    for y in range(Map.end):
        for x in range(Map.end):
            if Repair(player, y, x):
                repaired = True
    return repaired

def ReturnResources(player, resource , percent):
    for iType, iAmount in resource.iteritems():
        if iAmount > 0:
            rAmount = int(iAmount * percent/100.0)
            player.resources[iType] += rAmount
            Utility.SendMsg(player, iType.color + "Returning back " + str(rAmount) + " of "  + (iType.name) + "\n")
    
def ParseCommandFour(player, command):
    try:
        y1, x1, y2, x2, = map(int, re.findall(r'\d+', command))
        if 0 <= x1 < Map.end and 0 <= y1 < Map.end and \
           0 <= x2 < Map.end and 0 <= y2 < Map.end: 
            return True, y1, x1, y2, x2
        else:
            if not 0 <= x1 < Map.end:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value X1 out of range! X1 must be in range: 0 - " + str(Map.end - 1) + "\n")
                return False, 0, 0
            if not 0 <= x2 < Map.end:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value X2 out of range! X2 must be in range: 0 - " + str(Map.end - 1) + "\n")
                return False, 0, 0
            if not 0 <= y1 < Map.end:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value Y1 out of range! Y1 must be in range: 0 - " + str(Map.end - 1) + "\n")
                return False, 0, 0
            if not 0 <= y2 < Map.end:
                Utility.SendMsg(player, Colors.COLOR_RED + \
                                "Value Y2 out of range! Y2 must be in range: 0 - " + str(Map.end - 1) + "\n")
                return False, 0, 0
    except ValueError:
        Utility.SendMsg(player, Colors.COLOR_RED + "Bad number of arguments! Provide exactly four arguments!\n")
        return False, 0, 0, 0, 0

def MoveUnit(player, wy, wx, y1, x1, y2, x2):        
    pos2 = Pos(wy, wx, y2, x2)
    field2 = Map.Get(pos2)
    pos1 = Pos(wy, wx, y1, x1)
    field1 = Map.Get(pos1)
    if isinstance(field2, Buildings.Empty):
        if isinstance(field1, Units.Unit):
            Map.Swap(pos1, pos2)
            Utility.SendMsg(player, Colors.COLOR_GREEN + field1.__class__.__name__ +" succesfully moved!\n")
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Only units can be moved!\n") 
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Destination place is not empty!\n")

def MoveUnits(player, wy, wx, geo):
    if geo == Geo.NORTH:
        startX = Map.firstQ
        stopX = Map.thirdQ
        startY = 0
        stopY = Map.firstQ
        moveX = 0
        moveY = -Map.firstQ
    elif geo == Geo.SOUTH:
        startX = Map.firstQ
        stopX = Map.thirdQ
        startY = Map.thirdQ
        moveX = 0
        moveY = Map.firstQ
        stopY = Map.end
    elif geo == Geo.EAST:
        startX = Map.thirdQ
        stopX = Map.end
        startY = Map.firstQ
        stopY = Map.thirdQ
        moveX = Map.firstQ
        moveY = 0
    elif geo == Geo.WEST:
        startX = 0
        stopX = Map.firstQ
        startY = Map.firstQ
        stopY = Map.thirdQ
        moveX = -Map.firstQ
        moveY = 0
    for y in range(startY, stopY):
        for x in range(startX, stopX):
            pos1 = Pos(wy, wx, y, x)
            field1 = Map.Get(pos1)
            if isinstance(field1, Units.Unit):
                MoveUnit(player, wy, wx, y, x, y + moveY, x + moveX)

def OvertakeFortress(player, wy, wx):
    entity_list = []
    for y in range(Map.end):
        for x in range(Map.end):
            pos = Pos(wy, wx, y, x)
            entity = Map.Get(pos)
            if entity.owner != player.username:
                if isinstance(entity, Units.Unit):
                    Map.SetEmpty(pos)
                elif isinstance(entity, Buildings.Building):
                    entity_list.append((entity, y, x))  
                    Map.SetEmpty(pos)                     
    Map.SetFort(player, wy, wx)
    for entity, y, x in entity_list:
        pos = Pos(wy, wx, y, x)
        Map.Set(player, entity.__class__, pos)

def UpgradeFortress(player):
    fort = Map.GetFort(player.wy, player.wx)
    level = fort.level
    if level <= len(Fortress.production_per_level):
        cost = Buildings.Fortress.cost_per_level[level-1]
        if player.Pay(cost, 100.0):
            Map.ChangeFortLevel(player.wy, player.wx, 1)
            Utility.SendMsg(player, Colors.COLOR_GREEN + "Successfully upgraded fortress!\n")
    else:
        Utility.SendMsg(player, Colors.COLOR_GREEN + "Fortress maximally upgraded!\n")
        
def ShowDetailInfo(player, y, x):
    pos = Pos(player.wy, player.wx, y, x)
    field = Map.Get(pos)
    if not isinstance(field, Buildings.Empty) and not isinstance(field, Buildings.Forbidden):
        if isinstance(field, Buildings.Building):
            Buildings.ShowInfo(player, field)
        elif isinstance(field, Units.Unit):
            Units.ShowInfo(player, field)
    else:
        Utility.SendMsg(player, Colors.COLOR_RED + "Field is empty!\n")
    