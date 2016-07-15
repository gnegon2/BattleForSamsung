from Control import Control

class MenuCommands():
    REGISTER = "Register"
    LOGIN = "Login"
    EXIT = "Exit"
    
    @staticmethod
    def Get():
        commands = Control.CTRL_COLOR_ORANGE
        commands += MenuCommands.REGISTER + "\n"
        commands += MenuCommands.LOGIN + "\n"
        commands += MenuCommands.EXIT + "\n"
        return commands

class MainCommands:
    SHOW_MAP = "ShowMap"
    SHOW_RESOURCES = "ShowResources"
    RETURN = "Return"
    EXIT = "Exit"
    
    @staticmethod
    def Get():
        commands = Control.CTRL_COLOR_STEEL
        commands += MainCommands.SHOW_MAP + "\n"
        commands += MainCommands.SHOW_RESOURCES + "\n"
        commands += MainCommands.RETURN + "\n"
        commands += MainCommands.EXIT + "\n"
        return commands
    
class WorldMapCommands:
    GET_PRODUCTION = "GetProduction"
    ENTER_FORTRESS = "EnterFortress"
    SETTLE_FORTRESS = "SettleFortress"
    SHOW_FORTRESS_INFO = "ShowFortressInfo"
    ATTACK_FORTRESS = "AttackFortress"
    
    @staticmethod
    def Get():
        commands = Control.CTRL_COLOR_VIOLET
        commands += WorldMapCommands.GET_PRODUCTION + "\n"
        commands += WorldMapCommands.SHOW_FORTRESS_INFO + "\n"
        commands += WorldMapCommands.ENTER_FORTRESS + " Y X\n"
        commands += WorldMapCommands.SETTLE_FORTRESS + " Y X\n"
        commands += WorldMapCommands.ATTACK_FORTRESS + " Y X\n"
        return commands
    
class LocalMapCommands:
    BUILDINGS = "Buildings"
    ARMY = "Army" 
    DESTROY = "Destroy"
    
    @staticmethod
    def Get():
        commands = Control.CTRL_COLOR_VIOLET
        commands += LocalMapCommands.BUILDINGS + "\n"
        commands += LocalMapCommands.ARMY + "\n"
        commands += LocalMapCommands.DESTROY + " Y X\n"
        return commands
    
class BuildingCommands:
    HOUSE = "House"
    BANK = "Bank"
    SAW_MILL = "SawMill"
    LIBRARY = "Library"
    MINE = "Mine"
    CRYSTAL_MINE = "CrystalMine"
    WALL = "Wall"
    TOWER = "Tower"
    
    @staticmethod
    def Get():
        commands = Control.CTRL_COLOR_ORANGE
        commands += BuildingCommands.HOUSE + "\n"
        commands += BuildingCommands.BANK + "\n"
        commands += BuildingCommands.SAW_MILL + "\n"
        commands += BuildingCommands.LIBRARY + "\n"
        commands += BuildingCommands.MINE + "\n"
        commands += BuildingCommands.CRYSTAL_MINE + "\n"
        commands += BuildingCommands.WALL + "\n"
        commands += BuildingCommands.TOWER + "\n"
        return commands
    
class UnitsCommands:
    MOVE_UNIT = "MoveUnit"
    PEASANT = "Peasant"
    ARCHER = "Archer"
    SWORDMAN = "Swordman"
    PIKEMAN = "Pikeman"
    CROSSBOWMAN = "Crossbowman"
    HORSEMAN = "Horseman"
    CATAPULT = "Catapult"
    CANNON = "Cannon"
    
    @staticmethod
    def Get(level):
        commands = Control.CTRL_COLOR_ORANGE
        commands += UnitsCommands.MOVE_UNIT + " Y1 X1 Y2 X2\n"
        commands += UnitsCommands.PEASANT + "\n"
        if level > 0:
            commands += UnitsCommands.ARCHER + "\n"
        if level > 1:
            commands += UnitsCommands.SWORDMAN + "\n"
        if level > 2:
            commands += UnitsCommands.PIKEMAN + "\n"
        if level > 3:
            commands += UnitsCommands.CROSSBOWMAN + "\n"
        if level > 4:
            commands += UnitsCommands.HORSEMAN + "\n"
        if level > 5:
            commands += UnitsCommands.CATAPULT + "\n"
        if level > 6:
            commands += UnitsCommands.CANNON + "\n"
        return commands

class ActionCommands:
    SHOW_INFO = "ShowInfo"
    CREATE = "Create"
    
    @staticmethod
    def Get():
        commands = Control.CTRL_COLOR_ORANGE
        commands += ActionCommands.SHOW_INFO + "\n"
        commands += ActionCommands.CREATE + " Y X\n"
        return commands
    
class BattleCommands:
    QUICK_BATTLE = "QuickBattle"
    MAKE_MOVE = "MakeMove"
    
    @staticmethod
    def Get():
        commands = Control.CTRL_COLOR_ORANGE
        commands += BattleCommands.QUICK_BATTLE + "\n"
        commands += BattleCommands.MAKE_MOVE + "\n"
        return commands
        
        