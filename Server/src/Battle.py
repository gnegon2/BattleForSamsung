from BattleMap import BattleMap
from LocalMapStruct import localMaps
from Commands import BattleCommands
import Config
import Log
import Buildings
import Utility
import Control
import Units
import Statistics
import Geo

class Battle():
    
    def __init__(self, attacker, defender, army, worldPosY, worldPosX):
        Log.Save("Init battle on field: "+ str(worldPosY) + " " + str(worldPosX) + "!\n")
        self.attacker = attacker
        self.defender = defender
        self.army = army
        self.worldPosY = worldPosY
        self.worldPosX = worldPosX
        self.central = localMaps[self.worldPosY][self.worldPosX]
        if self.army['OnNorth']:
            self.north = localMaps[self.worldPosY - 1][self.worldPosX]
    
    def Start(self):
        Log.Save("Start battle on field: "+ str(self.worldPosY) + " " + str(self.worldPosX) + "!\n")
        battleMap = BattleMap(self.attacker, self.army, self.worldPosY, self.worldPosX)
        
        battleMenu = Control.CTRL_COLOR_AZURE
        battleMenu += "Welcome in Battle Menu!\n"
        battleMenu += "available options are:\n"
        Utility.SendMsg(self.attacker, battleMenu)
        Utility.SendMsg(self.attacker, BattleCommands.Get())
        
        Utility.SendMsg(self.attacker, Control.CTRL_BATTLE_MENU)
        command = Utility.SendMsg(self.attacker, Control.CTRL_INPUT)
        
        self.AttackerInit()
        while True:
            if command == BattleCommands.MAKE_MOVE:
                battleMap.ShowBattleMap()
                command = Utility.SendMsg(self.attacker, Control.CTRL_INPUT)
            
            self.AttackerPrepare()
            while True:
                if not self.AttackerMove():
                    break
     
    def AttackerInit(self):
        print "AttackerInit\n"
        if self.army['OnNorth']:
            self.AttackerNorthInit() 
                      
    def AttackerNorthInit(self):
        print "AttackerNorthInit\n"
        for x in range(Config.localMapSize / 4, 3 * Config.localMapSize / 4):
            for y in range(3 * Config.localMapSize / 4, Config.localMapSize):
                instance = self.north.fields[y][x]
                if isinstance(instance, Units.Unit):
                    instance.army = Geo.NORTH
                    
    def AttackerPrepare(self):
        print "AttackerPrepare\n"
        if self.army['OnNorth']:
            self.AttackerNorthPrepare()
    
    def AttackerNorthPrepare(self):
        print "AttackerNorthPrepare\n"
        for x in range(Config.localMapSize / 4, 3 * Config.localMapSize / 4):
            for y in range(3 * Config.localMapSize / 4, Config.localMapSize):
                instance = self.north.fields[y][x]
                if isinstance(instance, Units.Unit):
                    instance.move = instance.statistics[Statistics.Speed]
                    instance.attacked = False
                    
        for x in range(Config.localMapSize / 4, 3 * Config.localMapSize / 4):
            for y in range(0, Config.localMapSize/2):
                instance = self.central.fields[y][x] 
                if isinstance(instance, Units.Unit) and instance.army == Geo.NORTH:
                    instance.move = instance.statistics[Statistics.Speed]
                    instance.attacked = False
     
    def AttackerMove(self):
        print "AttackerMove\n"
        moved = False
        if self.army['OnNorth']: 
            if self.AttackerNorthMove():
                moved = True
        return moved
        
    def AttackerNorthMove(self):
        print "AttackerNorthMove\n"
        moved = False
        print "Moving army on north"
        for x in range(Config.localMapSize / 4, 3 * Config.localMapSize / 4):
            for y in range(3 * Config.localMapSize / 4, Config.localMapSize):
                instance = self.north.fields[y][x] 
                if isinstance(instance, Units.Unit) and instance.move > 0:
                    nextField = y + 1
                    if nextField < Config.localMapSize:
                        destIns = self.north.fields[nextField][x] 
                        if isinstance(destIns, Buildings.Empty):
                            self.north.fields[nextField][x] = instance
                            self.north.fields[y][x] = Buildings.Empty()
                            instance.move -= 1
                            moved = True
                    else:
                        destIns = self.central.fields[0][x]
                        if isinstance(destIns, Buildings.Empty):
                            self.central.fields[0][x] = instance
                            self.north.fields[y][x] = Buildings.Empty()
                            instance.move -= 1
                            moved = True
        print "Moving north army on central"                       
        for x in range(Config.localMapSize / 4, 3 * Config.localMapSize / 4):
            for y in range(0, Config.localMapSize/2):
                instance = self.central.fields[y][x] 
                if isinstance(instance, Units.Unit) and instance.army == Geo.NORTH and instance.move > 0:
                    nextField = y + 1
                    if nextField < Config.localMapSize/2:
                        destIns = self.central.fields[nextField][x]
                        if isinstance(destIns, Buildings.Empty):
                            self.central.fields[nextField][x] = instance
                            self.central.fields[y][x] = Buildings.Empty()
                            instance.move -= 1
                            moved = True
                    else:
                        if x < Config.localMapSize/2:
                            nextField = x + 1
                            destIns = self.central.fields[y][nextField]
                            if isinstance(destIns, Buildings.Empty):
                                self.central.fields[nextField][x] = instance
                                self.central.fields[y][x] = Buildings.Empty()
                                instance.move -= 1
                                moved = True
                        elif x > Config.localMapSize/2:
                            nextField = x - 1
                            destIns = self.central.fields[y][nextField]
                            if isinstance(destIns, Buildings.Empty):
                                self.central.fields[nextField][x] = instance
                                self.central.fields[y][x] = Buildings.Empty()
                                instance.move -= 1
                                moved = True
        return moved
    
    def AttackerAttack(self):
        print "AttackerAttack\n"
        if self.army['OnNorth']:
            self.AttackerNorthAttack()
    
    def AttackerNorthAttack(self):
        print "AttackerNorthAttack\n"
        for x in range(Config.localMapSize / 4, 3 * Config.localMapSize / 4):
            for y in range(3 * Config.localMapSize / 4, Config.localMapSize):
                instance = self.north.fields[y][x] 
                if isinstance(instance, Units.Unit) and not instance.attacked:
                    succes, y_enemy, x_enemy = self.FindFirstEnemyNorth(y, x, instance.statistics[Statistics.Range])
                    
                    
    def FindFirstEnemyNorth(self, y, x, attack_range):
        for y_range in range(attack_range + 1):
            for x_range in (attack_range + 1):
                
        
                        
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
    
        
                    
        
        