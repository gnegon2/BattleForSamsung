from Commands import UnitsCommands
from Control import Control
from Control import Type
from Utility import Utility
from Buildings import Buildings

class Units():    

    @staticmethod
    def CommandToUnit(command):
        if command == UnitsCommands.PEASANT:
            return Units.Peasant()
        elif command == UnitsCommands.ARCHER:
            return Units.Archer()
        elif command == UnitsCommands.SWORDMAN:
            return Units.Swordman()
        elif command == UnitsCommands.PIKEMAN:
            return Units.Pikeman()
        elif command == UnitsCommands.CROSSBOWMAN:
            return Units.Crossbowman()
        elif command == UnitsCommands.HORSEMAN:
            return Units.Horseman()
        elif command == UnitsCommands.CATAPULT:
            return Units.Catapult()
        elif command == UnitsCommands.CANNON:
            return Units.Cannon()
        else:
            return Buildings.Empty()
    
    @staticmethod
    def Buy(player, unit):
        if player.resources.gold >= unit.gold:
            if player.resources.wood >= unit.wood:
                if player.resources.stone >= unit.stone:
                    if player.resources.crystals >= unit.crystals:
                        player.resources.gold  -= unit.gold
                        player.resources.wood  -= unit.wood
                        player.resources.stone -= unit.stone
                        player.resources.crystals -= unit.crystals
                        return True
                    Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You need " + str(unit.crystals - player.resources.crystals) + " more crystals!\n" )
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You need " + str(unit.stone - player.resources.stone) + " more stone!\n" )
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You need " + str(unit.wood - player.resources.wood) + " more wood!\n" )
        Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You need " + str(unit.gold - player.resources.gold) + " more gold!\n" )
        return False
        
    @staticmethod
    def ShowInfo(player, unit):
        Utility.SendMsg(player, Control.CTRL_COLOR_AZURE + unit.__class__.__name__ + ": \n")
        Utility.SendMsg(player, unit.ExtraInfo())
        Utility.SendMsg(player, Control.CTRL_COLOR_ORANGE + "Cost: \n")
        if hasattr(unit, 'gold'):
            Utility.SendMsg(player, Control.CTRL_COLOR_GOLD + "Gold: " + str(unit.gold) + "\n")
        if hasattr(unit, 'wood'):
            Utility.SendMsg(player, Control.CTRL_COLOR_BROWN + "Wood: " + str(unit.wood) + "\n")
        if hasattr(unit, 'stone'):
            Utility.SendMsg(player, Control.CTRL_COLOR_STEEL + "Stone: " + str(unit.stone) + "\n")
        if hasattr(unit, 'crystals'):
            Utility.SendMsg(player, Control.CTRL_COLOR_VIOLET + "Crystals: " + str(unit.crystals) + "\n")
            
        Utility.SendMsg(player, Control.CTRL_COLOR_ORANGE + "Statistics: \n")
        if hasattr(unit, 'hit_points'):
            Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Hit points: " + str(unit.hit_points) + "\n")
        if hasattr(unit, 'defence'):
            Utility.SendMsg(player, Control.CTRL_COLOR_STEEL + "Defence: " + str(unit.defence) + "\n")
        if hasattr(unit, 'attack'):
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Attack: " + str(unit.attack) + "\n")
        if hasattr(unit, 'min_damage'):
            Utility.SendMsg(player, Control.CTRL_COLOR_BROWN + "Min. damage: " + str(unit.min_damage) + "\n")
        if hasattr(unit, 'max_damage'):
            Utility.SendMsg(player, Control.CTRL_COLOR_VIOLET + "Max. damage: " + str(unit.max_damage) + "\n")
        if hasattr(unit, 'range'):
            Utility.SendMsg(player, Control.CTRL_COLOR_GOLD + "Range: " + str(unit.range) + "\n")    
        if hasattr(unit, 'speed'):
            Utility.SendMsg(player, Control.CTRL_COLOR_GOLD + "Speed: " + str(unit.speed) + "\n") 

    class Peasant():
        def __init__(self, player):
            self.field = "1"
            self.color = Control.CTRL_COLOR_GREEN
            self.type = Type.UNIT
            self.owner = player
            
            self.gold = 5
            
            self.hit_points = 10
            self.defence = 2
            self.attack = 1
            self.min_damage = 1
            self.max_damage = 2
            self.range = 1
            self.speed = 1
            
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Peasant is the stupid man with fork.\n"
            return extraInfoMsg
        
    class Archer():
        def __init__(self, player):
            self.field = "2"
            self.color = Control.CTRL_COLOR_GOLD
            self.type = Type.UNIT
            self.owner = player
            
            self.gold = 20
            
            self.hit_points = 20
            self.defence = 3
            self.attack = 2
            self.min_damage = 2
            self.max_damage = 4
            self.range = 3
            self.speed = 1
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Archer can attack on distance.\n"
            return extraInfoMsg
        
    class Swordman():
        def __init__(self, player):
            self.field = "3"
            self.color = Control.CTRL_COLOR_STEEL
            self.type = Type.UNIT
            self.owner = player
            
            self.gold = 50
            self.stone = 1
                    
            self.hit_points = 50
            self.defence = 8
            self.attack = 6
            self.min_damage = 5
            self.max_damage = 8
            self.range = 1
            self.speed = 1
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Swordman is a strong unit in armor.\n"
            return extraInfoMsg
        
    class Pikeman():
        def __init__(self, player):
            self.field = "4" 
            self.color = Control.CTRL_COLOR_GRANAT
            self.type = Type.UNIT
            self.owner = player
            
            self.gold = 70
            self.wood = 1
            
            self.hit_points = 70
            self.defence = 10
            self.attack = 7
            self.min_damage = 6
            self.max_damage = 12
            self.range = 2
            self.speed = 2
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Pikeman is best against horseman.\n"
            return extraInfoMsg
         
    class Crossbowman():
        def __init__(self, player):
            self.field = "5" 
            self.color = Control.CTRL_COLOR_ORANGE
            self.type = Type.UNIT
            self.owner = player
            
            self.gold = 80
            self.wood = 1
            self.stone = 1
            
            self.hit_points = 70
            self.defence = 8
            self.attack = 8
            self.min_damage = 10
            self.max_damage = 12
            self.range = 4
            self.speed = 2
            
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Crossbowman is a very strong range unit.\n"
            return extraInfoMsg
        
    class Horseman():
        def __init__(self, player):
            self.field = "6" 
            self.color = Control.CTRL_COLOR_BROWN
            self.type = Type.UNIT
            self.owner = player
            
            self.gold = 100
            self.wood = 2
            
            self.hit_points = 100
            self.defence = 15
            self.attack = 10
            self.min_damage = 12
            self.max_damage = 15
            self.range = 1
            self.speed = 4 
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Horseman is a very fast unit.\n"
            return extraInfoMsg
        
    class Catapult():
        def __init__(self, player):
            self.field = "7" 
            self.color = Control.CTRL_COLOR_BLOOD
            self.type = Type.UNIT
            self.owner = player
            
            self.gold = 150
            self.wood = 2
            self.stone = 2
            
            self.hit_points = 150
            self.defence = 12
            self.attack = 15
            self.min_damage = 15
            self.max_damage = 20
            self.range = 6 
            self.speed = 1
            
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Catapult can attack at very high distance.\n"
            return extraInfoMsg
        
    class Cannon():
        def __init__(self, player):
            self.field = "8" 
            self.color = Control.CTRL_COLOR_AZURE
            self.type = Type.UNIT
            self.owner = player
            
            self.gold = 200
            self.wood = 2
            self.stone = 2
            self.crystals = 1
            
            self.hit_points = 200
            self.defence = 20
            self.attack = 20
            self.min_damage = 20
            self.max_damage = 20
            self.range = 4
            self.speed = 2
            
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Cannon is the most powerfull unit.\n"
            return extraInfoMsg
