from BattleMap import BattleMap
from Commands import BattleCommands
from Colors import Colors
from Pos import Pos
import Log
import Buildings
import Utility
import Control
import Units
import Statistics
import Geo
import Map
import Commands
import random

class Battle():
    
    def __init__(self, attacker, army, wy, wx):
        Log.Save("Init battle on field: "+ str(wy) + " " + str(wx) + "!\n")
        self.attacker = attacker
        self.army = army
        self.cwy = wy
        self.cwx = wx
        if self.army[Geo.NORTH]:
            self.nwy = wy - 1
            self.nwx = wx
        if self.army[Geo.SOUTH]:
            self.swy = wy + 1
            self.swx = wx
        if self.army[Geo.EAST]:
            self.ewy = wy
            self.ewx = wx + 1
        if self.army[Geo.WEST]:
            self.wwy = wy
            self.wwx = wx - 1
    
    def Start(self):
        Log.Save("Start battle on field: "+ str(self.cwy) + " " + str(self.cwx) + "!\n")
        battleMap = BattleMap(self.attacker, self.army, self.cwy, self.cwx)
        
        battleMenu = Colors.COLOR_AZURE
        battleMenu += "Welcome in Battle Menu!\n"
        battleMenu += "available options are:\n"
        Utility.SendMsg(self.attacker, battleMenu)
        Utility.SendMsg(self.attacker, Commands.GetCommands(BattleCommands))
        
        Utility.SendMsg(self.attacker, Control.CTRL_MENU_BATTLE)
        command = Utility.SendMsg(self.attacker, Control.CTRL_INPUT)
        
        self.AttackerInit()
        while True:
            if command == BattleCommands._1_0_MAKE_MOVE:
                battleMap.ShowBattleMap()
                command = Utility.SendMsg(self.attacker, Control.CTRL_INPUT)
            
            self.AttackerPrepare()
            self.AttackerAttack()
            while True:
                if not self.AttackerMove():
                    break
            
            if self.AttackerAttack():
                return True
     
    def AttackerInit(self):
        print "AttackerInit\n"
        if self.army[Geo.NORTH]:
            self.AttackerNorthInit() 
                      
    def AttackerNorthInit(self):
        print "AttackerNorthInit\n"
        for x in range(Map.firstQ, Map.thirdQ):
            for y in range(Map.thirdQ, Map.end):
                instance = Map.Get(Pos(self.nwy, self.nwx, y, x))
                if isinstance(instance, Units.Unit):
                    instance.army = Geo.NORTH
                    
    def AttackerPrepare(self):
        print "AttackerPrepare\n"
        if self.army[Geo.NORTH]:
            self.AttackerNorthPrepare()
    
    def AttackerNorthPrepare(self):
        print "AttackerNorthPrepare\n"
        for x in range(Map.firstQ, Map.thirdQ):
            for y in range(Map.thirdQ, Map.end + Map.half):
                instance = Map.Get(Pos(self.nwy, self.nwx, y, x))
                if isinstance(instance, Units.Unit) and instance.owner == self.attacker and instance.army == Geo.NORTH:
                    instance.move = instance.statistics[Statistics.Speed]
                    instance.attacked = False
     
    def AttackerMove(self):
        print "AttackerMove\n"
        moved = False
        if self.army[Geo.NORTH]: 
            if self.AttackerNorthMove():
                moved = True
        return moved
        
    def AttackerNorthMove(self):
        print "AttackerNorthMove\n"
        moved = False       
        for x in range(Map.firstQ, Map.thirdQ):
            for y in range(Map.thirdQ, Map.end + Map.half - 1):
                pos1 = Pos(self.nwy, self.nwx, y, x)
                instance = Map.Get(pos1)
                if isinstance(instance, Units.Unit) and instance.owner == self.attacker \
                    and instance.army == Geo.NORTH and instance.move > 0:
                    pos2 = Pos(self.nwy, self.nwx, y + 1, x)
                    destIns = Map.Get(pos2)
                    if isinstance(destIns, Buildings.Empty):
                        Map.Swap(pos1, pos2)
                        instance.move -= 1
                        moved = True
        
        for x in range(Map.firstQ, Map.thirdQ):
            pos1 = Pos(self.cwy, self.cwx, Map.half, x)
            instance = Map.Get(pos1)
            if isinstance(instance, Units.Unit) and instance.owner == self.attacker \
                and instance.army == Geo.NORTH and instance.move > 0:
                    if x < Map.half:
                        nextField = x + 1
                        pos2 = Pos(self.cwy, self.cwx, nextField, x)
                        destIns = Map.Get(pos2)
                        if isinstance(destIns, Buildings.Empty):
                            Map.Swap(pos1, pos2)
                            instance.move -= 1
                            moved = True
                    elif x > Map.half:
                        nextField = x - 1
                        pos2 = Pos(self.cwy, self.cwx, nextField, x)
                        destIns = Map.Get(pos2)
                        if isinstance(destIns, Buildings.Empty):
                            Map.Swap(pos1, pos2)
                            instance.move -= 1
                            moved = True

        return moved
    
    def AttackerAttack(self):
        print "AttackerAttack\n"
        if self.army[Geo.NORTH]:
            if self.AttackerNorthAttack():
                return True
    
    def AttackerNorthAttack(self):
        print "AttackerNorthAttack\n"
        for x in range(Map.firstQ, Map.thirdQ):
            for y in range(Map.thirdQ, Map.end + Map.half):
                pos1 = Pos(self.nwy, self.nwx, y, x)
                instance = Map.Get(pos1)
                if isinstance(instance, Units.Unit) and instance.owner == self.attacker and \
                    instance.army == Geo.NORTH and not instance.attacked:
                    succes, pos_e = self.FindFirstEnemyNorth(pos1, instance.statistics[Statistics.Range])
                    if succes:
                        enemyIns = Map.Get(pos_e)
                        self.TakeDamage(instance, enemyIns)
                        instance.attacked = True
                        instance.move = 0
                        if enemyIns.statistics[Statistics.HitPoints] <= 0:
                            print "enemy destroyed!"
                            if isinstance(enemyIns, Buildings.Fortress):
                                print "victory!"
                                return True
                            else:
                                Map.SetEmpty(pos_e)
                        print "succes"
        return False
                        
    def TakeDamage(self, attacker_unit, enemy_unit):
        print "attacker_unit =", attacker_unit
        print "enemy_unit =", enemy_unit
        damage_range = attacker_unit.statistics[Statistics.MaxDamage] - attacker_unit.statistics[Statistics.MinDamage]
        print "damage_range =",damage_range
        damage = attacker_unit.statistics[Statistics.Attack] * (attacker_unit.statistics[Statistics.MinDamage] + random.randint(0, damage_range))
        print "enemy_unit.statistics[Statistics.HitPoints] =",enemy_unit.statistics[Statistics.HitPoints]
        print "damage =",damage
        enemy_unit.statistics[Statistics.HitPoints] -= int(round(float(damage / enemy_unit.statistics[Statistics.Defence])))
        print "enemy_unit.statistics[Statistics.HitPoints] =",enemy_unit.statistics[Statistics.HitPoints]
                    
    def FindFirstEnemyNorth(self, pos, attack_range):
        print "FindFirstEnemyNorth\n"
        for y_range in range(attack_range + 1):
            for x_range in range(attack_range + 1):
                print y_range, x_range
                pos_e = Pos(pos.wy, pos.wx, pos.y + y_range, pos.x + x_range)
                instance = Map.Get(pos_e)
                if isinstance(instance, Units.Unit) or isinstance(instance, Buildings.Building):
                    if instance.owner != self.attacker:
                        print "Enemy founded at: " + str(pos_e.y) + " " + str(pos_e.x) + "\n"
                        return True, pos_e
                pos_e = Pos(pos.wy, pos.wx, pos.y + y_range, pos.x - x_range)
                instance = Map.Get(pos_e)
                if isinstance(instance, Units.Unit) or isinstance(instance, Buildings.Building):
                    if instance.owner != self.attacker:
                        print "Enemy founded at: " + str(pos_e.y) + " " + str(pos_e.x) + "\n"
                        return True, pos_e
        return False, 0
                
                
