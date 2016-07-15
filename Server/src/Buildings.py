from Utility import Utility
from Control import Control
from Control import Type
from Resources import Resources
from Commands import BuildingCommands
from LocalMapStruct import localMaps

class Buildings():

    @staticmethod
    def CommandToBuilding(player, command):
        if command == BuildingCommands.BANK:
            return Buildings.Bank(player)
        elif command == BuildingCommands.HOUSE:
            return Buildings.House(player)
        elif command == BuildingCommands.SAW_MILL:
            return Buildings.SawMill(player)
        elif command == BuildingCommands.LIBRARY:
            return Buildings.Library(player)
        elif command == BuildingCommands.MINE:
            return Buildings.Mine(player)
        elif command == BuildingCommands.CRYSTAL_MINE:
            return Buildings.CrystalMine(player)
        elif command == BuildingCommands.WALL:
            return Buildings.Wall(player)
        elif command == BuildingCommands.TOWER:
            return Buildings.Tower(player)
        else:
            return Buildings.Empty()
        
    @staticmethod
    def Build(player, building):
        if not hasattr(building, 'gold') or (hasattr(building, 'gold') and player.resources.gold >= building.gold):
            if not hasattr(building, 'wood') or (hasattr(building, 'wood') and player.resources.wood >= building.wood):
                if not hasattr(building, 'stone') or (hasattr(building, 'stone') and player.resources.stone >= building.stone):
                    if not hasattr(building, 'crystals') or (hasattr(building, 'crystals') and player.resources.crystals >= building.crystals):
                        player.resources.gold  -= building.gold
                        player.resources.wood  -= building.wood
                        player.resources.stone -= building.stone
                        player.resources.crystals -= building.crystals
                        return True
                    Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You need " + str(building.crystals - player.resources.crystals) + " more crystals!\n" )
                    return False
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You need " + str(building.stone - player.resources.stone) + " more stone!\n" )
                return False
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You need " + str(building.wood - player.resources.wood) + " more wood!\n" )
            return False
        Utility.SendMsg(player, Control.CTRL_COLOR_RED + "You need " + str(building.gold - player.resources.gold) + " more gold!\n" )
        return False
    
    @staticmethod
    def ShowInfo(player, building):
        Utility.SendMsg(player, Control.CTRL_COLOR_AZURE + building.__class__.__name__ + ": \n")
        Utility.SendMsg(player, building.ExtraInfo())
        Utility.SendMsg(player, Control.CTRL_COLOR_ORANGE + "Cost: \n")
        if hasattr(building, 'gold'):
            Utility.SendMsg(player, Control.CTRL_COLOR_GOLD + "Gold: " + str(building.gold) + "\n")
        if hasattr(building, 'wood'):
            Utility.SendMsg(player, Control.CTRL_COLOR_BROWN + "Wood: " + str(building.wood) + "\n")
        if hasattr(building, 'stone'):
            Utility.SendMsg(player, Control.CTRL_COLOR_STEEL + "Stone: " + str(building.stone) + "\n")
        if hasattr(building, 'crystals'):
            Utility.SendMsg(player, Control.CTRL_COLOR_VIOLET + "Crystals: " + str(building.crystals) + "\n")
        
        Utility.SendMsg(player, Control.CTRL_COLOR_ORANGE + "Production: \n")
        if hasattr(building, 'gold_production'):
            Utility.SendMsg(player, Control.CTRL_COLOR_GOLD + "Gold: " + str(building.gold_production) + "\n")
        if hasattr(building, 'wood_production'):
            Utility.SendMsg(player, Control.CTRL_COLOR_BROWN + "Wood: " + str(building.wood_production) + "\n")
        if hasattr(building, 'stone_production'):
            Utility.SendMsg(player, Control.CTRL_COLOR_STEEL + "Stone: " + str(building.stone_production) + "\n")
        if hasattr(building, 'crystals_production'):
            Utility.SendMsg(player, Control.CTRL_COLOR_VIOLET + "Crystals: " + str(building.crystals_production) + "\n")
        
        Utility.SendMsg(player, Control.CTRL_COLOR_ORANGE + "Statistics: \n")
        if hasattr(building, 'hit_points'):
            Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Hit points: " + str(building.hit_points) + "\n")
        if hasattr(building, 'defence'):
            Utility.SendMsg(player, Control.CTRL_COLOR_STEEL + "Defence: " + str(building.defence) + "\n")
        if hasattr(building, 'attack'):
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Attack: " + str(building.attack) + "\n")
        if hasattr(building, 'min_damage'):
            Utility.SendMsg(player, Control.CTRL_COLOR_BROWN + "Min. damage: " + str(building.min_damage) + "\n")
        if hasattr(building, 'max_damage'):
            Utility.SendMsg(player, Control.CTRL_COLOR_VIOLET + "Max. damage: " + str(building.max_damage) + "\n")
        if hasattr(building, 'range'):
            Utility.SendMsg(player, Control.CTRL_COLOR_GOLD + "Range: " + str(building.range) + "\n")      
        
        
    @staticmethod
    def GetProduction(player, building):
        Utility.SendMsg(player, Control.CTRL_COLOR_AZURE + building.__class__.__name__ + " produce: \n")
        if hasattr(building, 'gold_production'):
            Utility.SendMsg(player, Control.CTRL_COLOR_GOLD + "Gold: " + str(building.gold_production) + "\n")
            player.resources.Add(Resources.GOLD, building.gold_production)
        if hasattr(building, 'wood_production'):
            Utility.SendMsg(player, Control.CTRL_COLOR_BROWN + "Wood: " + str(building.wood_production) + "\n")
            player.resources.Add(Resources.WOOD, building.wood_production)
        if hasattr(building, 'stone_production'):
            Utility.SendMsg(player, Control.CTRL_COLOR_STEEL + "Stone: " + str(building.stone_production) + "\n")
            player.resources.Add(Resources.STONE, building.stone_production)
        if hasattr(building, 'crystals_production'):
            Utility.SendMsg(player, Control.CTRL_COLOR_VIOLET + "Crystals: " + str(building.crystals_production) + "\n")
            player.resources.Add(Resources.CRYSTALS, building.crystals_production)

    class Empty():
        def __init__(self):
            self.field = "0"
            self.color = Control.CTRL_COLOR_BROWN
            self.type = Type.EMPTY
            
    class Forbidden():
        def __init__(self):
            self.field = "X"
            self.color = Control.CTRL_COLOR_POPPY
            self.type = Type.FORBIDDEN
    
    class Fortress():
        def __init__(self, player):
            self.field = "F"
            self.color = Control.CTRL_COLOR_POPPY
            self.type = Type.BUILDING
            self.owner = player
            
            self.hit_points = 1000 
            self.defence = 100
            self.attack = 10 
            self.min_damage = 5 
            self.max_damage = 10 
            self.range = 1 
             
            self.gold = 200
            self.wood = 5
            self.stone = 5
            self.crystals = 1
            
            self.gold_production = 40
            self.wood_production = 2
            self.stone_production = 2
            
            self.army_production = 5
            
            self.owner.info.maxNumberOfUnits += self.army_production
            
        def __del__(self):
            self.owner.info.maxNumberOfUnits -= self.army_production
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Fortress is the main building on the map.\n"
            return extraInfoMsg
        
    class Bank():
        def __init__(self, player):
            self.field = "B" 
            self.color = Control.CTRL_COLOR_GOLD
            self.type = Type.BUILDING
            self.owner = player
            
            self.hit_points = 100
            self.defence = 20
            
            self.gold = 40
            self.wood = 5
            self.stone = 5
            
            self.gold_production = 60
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Each bank provide you a lot of money.\n"
            return extraInfoMsg
        
    class House():
        def __init__(self, player):
            self.field = "H"
            self.color = Control.CTRL_COLOR_GREEN
            self.type = Type.BUILDING
            self.owner = player
            
            self.hit_points = 250
            self.defence = 30
            
            self.gold = 50
            self.wood = 4
            self.stone = 2
            
            self.army_production = 5
            
            self.owner.info.maxNumberOfUnits += self.army_production
            print self.owner.info.maxNumberOfUnits
        
        def __del__(self):
            self.owner.info.maxNumberOfUnits -= self.army_production   
            print self.owner.info.maxNumberOfUnits 
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Each house provide you to recruit more army.\n"
            extraInfoMsg += "Army production bonus: "
            extraInfoMsg += str(Buildings.House.army_production) + "\n"
            return extraInfoMsg
        
    class SawMill():
        def __init__(self, player):
            self.field = "S"
            self.color = Control.CTRL_COLOR_WOOD
            self.type = Type.BUILDING
            self.owner = player
            
            self.hit_points = 200
            self.defence = 25
            
            self.gold = 40
            self.wood = 5

            self.wood_production = 5
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Saw mill provide you a lot of wood.\n"
            return extraInfoMsg
        
    class Library():
        def __init__(self, player):
            self.field = "L"
            self.color = Control.CTRL_COLOR_AZURE
            self.type = Type.BUILDING
            self.owner = player
            
            self.hit_points = 50
            self.defence = 10
            
            self.gold = 150
            self.wood = 4
            self.stone = 4
            self.crystals = 1
            
            localMaps[self.owner.localMapY][self.owner.localMapX].librariesCount += 1
            print localMaps[self.owner.localMapY][self.owner.localMapX].librariesCount
            
        def __del__(self):
            localMaps[self.owner.localMapY][self.owner.localMapX].librariesCount -= 1  
            print localMaps[self.owner.localMapY][self.owner.localMapX].librariesCount
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Each library give you access to a new unit.\n"
            return extraInfoMsg
        
    class Mine():
        def __init__(self, player):
            self.field = "M"
            self.color = Control.CTRL_COLOR_STEEL
            self.type = Type.BUILDING
            self.owner = player
            
            self.hit_points = 100
            self.defence = 20

            self.gold = 60
            self.wood = 4
            
            self.stone_production = 5
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Mine provide you a lot of stone.\n"
            return extraInfoMsg
        
    class CrystalMine():
        def __init__(self, player):
            self.field = "C"
            self.color = Control.CTRL_COLOR_VIOLET
            self.type = Type.BUILDING
            self.owner = player
            
            self.hit_points = 150
            self.defence = 30
            
            self.gold = 200
            self.wood = 4
            self.stone = 4
            
            self.crystals_production = 1
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Crystal mine provide you a crystals.\n"
            return extraInfoMsg
        
    class Wall():
        def __init__(self, player):
            self.field = "W"
            self.color = Control.CTRL_COLOR_GRANAT
            self.type = Type.BUILDING
            self.owner = player
            
            self.hit_points = 500
            self.defence = 50
            
            self.gold = 40
            self.wood = 1
            self.stone = 1
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Wall defends your fortress.\n"
            return extraInfoMsg
        
    class Tower():
        def __init__(self, player):
            self.field = "T"
            self.color = Control.CTRL_COLOR_BLOOD
            self.type = Type.BUILDING
            self.owner = player
            
            self.hit_points = 700
            self.defence = 60
            self.attack = 20
            self.min_damage = 10
            self.max_damage = 20
            self.range = 3
            
            self.gold = 120
            self.wood = 3
            self.stone = 3
        
        @staticmethod
        def ExtraInfo():
            extraInfoMsg = Control.CTRL_COLOR_GREEN
            extraInfoMsg += "Tower attack nearby enemy and defends your fortress.\n"
            return extraInfoMsg