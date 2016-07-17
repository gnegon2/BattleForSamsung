from Colors import Colors
import Control

def ControlToCommands(data):
    if data.find(Control.CTRL_MENU_MAIN) != -1:
        return MenuCommands
    elif data.find(Control.CTRL_MENU_WORLD_MAP) != -1:
        return WorldMapCommands
    elif data.find(Control.CTRL_MENU_LOCAL_MAP) != -1:
        return LocalMapCommands
    elif data.find(Control.CTRL_MENU_BUILDING) != -1:
        return BuildingCommands
    elif data.find(Control.CTRL_MENU_UNITS) != -1:
        return UnitsCommands
    elif data.find(Control.CTRL_MENU_ACTION) != -1:
        return ActionCommands
    elif data.find(Control.CTRL_MENU_BATTLE) != -1:
        return BattleCommands
    elif data.find(Control.CTRL_MENU_SCOUTING_MODE) != -1:
        return ScoutingCommands
    else:
        return Empty

class Empty():
    
    @staticmethod
    def Color():
        return Colors.COLOR_WHITE
    
class MenuCommands():
    _0_0_REGISTER = "Register"
    _1_0_LOGIN = "Login"
    _2_0_EXIT = "Exit"
    
    @staticmethod
    def Color():
        return Colors.COLOR_ORANGE

class MainCommands:
    _0_0_SHOW_MAP = "ShowMap"
    _1_0_SHOW_RESOURCES = "ShowResources"
    _2_0_RETURN = "Return"
    _3_0_EXIT = "Exit"
    
    @staticmethod
    def Color():
        return Colors.COLOR_STEEL
    
class WorldMapCommands:
    _0_0_SHOW_FORTRESS_INFO = "ShowFortressInfo"
    _1_2_SETTLE_FORTRESS = "SettleFortress"
    _2_2_ENTER_FORTRESS = "EnterFortress"
    _3_0_GET_PRODUCTION = "GetProduction"
    _4_2_ATTACK_FORTRESS = "AttackFortress"
    
    @staticmethod
    def Color():
        return Colors.COLOR_VIOLET
    
class LocalMapCommands:
    _0_0_BUILDINGS = "Buildings"
    _1_0_ARMY = "Army" 
    _2_2_DESTROY = "Destroy"
    
    @staticmethod
    def Color():
        return Colors.COLOR_VIOLET
    
class BuildingCommands:
    _0_0_HOUSE = "House"
    _1_0_BANK = "Bank"
    _2_0_SAW_MILL = "SawMill"
    _3_0_MINE = "Mine"
    _4_0_CRYSTAL_MINE = "CrystalMine"
    _5_0_WALL = "Wall"
    _6_0_TOWER = "Tower"
    _7_0_LIBRARY = "Library"
    
    @staticmethod
    def Color():
        return Colors.COLOR_ORANGE
    
class UnitsCommands:
    _0_4_MOVE_UNIT = "MoveUnit"
    _1_0_PEASANT = "Peasant"
    _2_0_ARCHER = "Archer"
    _3_0_SWORDMAN = "Swordman"
    _4_0_PIKEMAN = "Pikeman"
    _5_0_CROSSBOWMAN = "Crossbowman"
    _6_0_HORSEMAN = "Horseman"
    _7_0_CATAPULT = "Catapult"
    _8_0_CANNON = "Cannon"
    
    @staticmethod
    def Color():
        return Colors.COLOR_ORANGE

class ActionCommands:
    _0_0_SHOW_INFO = "ShowInfo"
    _1_2_CREATE = "Create"
    
    @staticmethod
    def Color():
        return Colors.COLOR_ORANGE
    
class BattleCommands:
    _0_0_QUICK_BATTLE = "QuickBattle"
    _1_0_MAKE_MOVE = "MakeMove"
    
    @staticmethod
    def Color():
        return Colors.COLOR_ORANGE

class ScoutingCommands:
    _0_0_SHOW_ENEMY_INFO = "ShowEnemyInfo"
    
    @staticmethod
    def Color():
        return Colors.COLOR_BLOOD

def GetCommands(commands):
    msg = ""
    for key, value in sorted(vars(commands).iteritems()):
        if not (key.startswith('__')) and isinstance(value, basestring):
            if key[3] == "0":
                msg += commands.Color() + value + "\n"
            elif key[3] == "2":
                msg += commands.Color() + value + " Y X\n"
            elif key[3] == "4":
                msg += commands.Color() + value + " Y1 X1 Y2 X2\n" 
    return msg  

def GetUnitCommands(level):
    msg = ""
    for key, value in sorted(vars(UnitsCommands).iteritems()):
        if not (key.startswith('__')) and isinstance(value, basestring):
            unit_level = int(key[1])
            if unit_level <= level:
                msg += UnitsCommands.Color() + value + "\n" 
    return msg  
        