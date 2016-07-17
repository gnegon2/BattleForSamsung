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
        
        self.InitBattle()
        while True:
            if command == BattleCommands._1_0_MAKE_MOVE:
                battleMap.ShowBattleMap()
                command = Utility.SendMsg(self.attacker, Control.CTRL_INPUT)
                self.log = True
            else:
                self.log = False
            
            self.PrepareBattle()
            if self.Attack():
                return True
            while True:
                if not self.AttackerMove():
                    break
            if self.Attack():
                return True
            
            if not self.CheckUnits():
                return False
     
    def InitEntity(self, wy, wx, y, x, geo):
        entity = Map.Get(Pos(wy, wx, y, x))
        if isinstance(entity, Units.Unit) or isinstance(entity, Buildings.Building):
            entity.army = geo
                      
    def InitBattle(self):
        print "InitBattle\n"
        # Attacker
        if self.army[Geo.NORTH]:
            for x in range(Map.firstQ, Map.thirdQ):
                for y in range(Map.thirdQ, Map.end):
                    self.InitEntity(self.nwy, self.nwx, y, x, Geo.NORTH)
        if self.army[Geo.SOUTH]:
            for x in range(Map.firstQ, Map.thirdQ):
                for y in range(Map.firstQ):
                    self.InitEntity(self.swy, self.swx, y, x, Geo.SOUTH)
        if self.army[Geo.EAST]:
            for x in range(Map.firstQ):
                for y in range(Map.firstQ, Map.thirdQ):
                    self.InitEntity(self.ewy, self.ewx, y, x, Geo.EAST)
        if self.army[Geo.WEST]:
            for x in range(Map.thirdQ, Map.end):
                for y in range(Map.firstQ, Map.thirdQ):
                    self.InitEntity(self.wwy, self.wwx, y, x, Geo.WEST)         
        # Defender
        for x in range(Map.end):
            for y in range(Map.end):
                self.InitEntity(self.cwy, self.cwx, y, x, Geo.CENTRAL)
    
    def PrepareEntity(self, wy, wx, y, x):
        entity = Map.Get(Pos(wy, wx, y, x))
        if isinstance(entity, Units.Unit) or isinstance(entity, Buildings.Building):
            if isinstance(entity, Units.Unit):
                entity.move = entity.statistics[Statistics.Speed]
            entity.attacked = False
    
    def PrepareBattle(self):
        print "PrepareBattle\n"
        if self.army[Geo.NORTH]:
            for x in range(Map.firstQ, Map.thirdQ):
                for y in range(Map.thirdQ, Map.end):
                    self.PrepareEntity(self.nwy, self.nwx, y, x)
        if self.army[Geo.SOUTH]:
            for x in range(Map.firstQ, Map.thirdQ):
                for y in range(Map.firstQ):
                    self.PrepareEntity(self.swy, self.swx, y, x)
        if self.army[Geo.EAST]:
            for x in range(Map.firstQ):
                for y in range(Map.firstQ, Map.thirdQ):
                    self.PrepareEntity(self.ewy, self.ewx, y, x)
        if self.army[Geo.WEST]:
            for x in range(Map.thirdQ, Map.end):
                for y in range(Map.firstQ, Map.thirdQ):
                    self.PrepareEntity(self.wwy, self.wwx, y, x)
                    
        # Defender
        for x in range(Map.end):
            for y in range(Map.end):
                self.PrepareEntity(self.cwy, self.cwx, y, x)
    
    def MoveUnit(self, wy, wx,y, x):
        src_pos = Pos(wy, wx, y, x)
        unit = Map.Get(src_pos)
        if isinstance(unit, Units.Unit) and unit.owner == self.attacker and unit.move > 0:
            if unit.army == Geo.NORTH:
                ny, nx = y+1, x
            elif unit.army == Geo.SOUTH:
                ny, nx = y-1, x
            elif unit.army == Geo.EAST:
                ny, nx = y, x-1
            elif unit.army == Geo.WEST:
                ny, nx = y, x+1
            dst_pos = Pos(wy, wx, ny, nx)
            field = Map.Get(dst_pos)
            if isinstance(field, Buildings.Empty):
                Map.Swap(src_pos, dst_pos)
                unit.move -= 1
                return True
        return False
    
    def ChangeGeo(self, wy, wx, y, x):
        src_pos = Pos(wy, wx, y, x)
        unit = Map.Get(src_pos)
        if isinstance(unit, Units.Unit) and unit.owner == self.attacker:
            if x == Map.half or x == Map.half - 1:
                if y < Map.half:
                    unit.army = Geo.NORTH
                else:
                    unit.army = Geo.SOUTH
            if y == Map.half or y == Map.half - 1:
                if x > Map.half:
                    unit.army = Geo.EAST
                else:
                    unit.army = Geo.WEST
        
    def AttackerMove(self):
        print "AttackerMove\n"
        moved = False  
        if self.army[Geo.NORTH]: 
            for x in range(Map.firstQ, Map.thirdQ):
                for y in range(Map.thirdQ, Map.end):
                    if self.MoveUnit(self.nwy, self.nwx, y, x):
                        moved = True
        if self.army[Geo.SOUTH]:
            for x in range(Map.firstQ, Map.thirdQ):
                for y in range(Map.firstQ):
                    if self.MoveUnit(self.swy, self.swx, y, x):
                        moved = True
        if self.army[Geo.EAST]:
            for x in range(Map.firstQ):
                for y in range(Map.firstQ, Map.thirdQ):
                    if self.MoveUnit(self.ewy, self.ewx, y, x):
                        moved = True
        if self.army[Geo.WEST]:
            for x in range(Map.thirdQ, Map.end):
                for y in range(Map.firstQ, Map.thirdQ):
                    if self.MoveUnit(self.wwy, self.wwx, y, x):
                        moved = True
        for x in range(Map.end):
            for y in range(Map.end):
                if self.MoveUnit(self.cwy, self.cwx, y, x):
                    moved = True
                self.ChangeGeo(self.cwy, self.cwx, y, x)
        return moved
    
    def EntityAttack(self, wy, wx, y, x):
        src_pos = Pos(wy, wx, y, x)
        entity = Map.Get(src_pos)  
        if (isinstance(entity, Units.Unit) or isinstance(entity, Buildings.Building)) and not entity.attacked:
            attack_range = entity.statistics[Statistics.Range]
            if attack_range > 0:
                succes, dst_pos = self.FindEnemy(src_pos, entity)
                if succes:
                    enemy_entity = Map.Get(dst_pos)
                    self.TakeDamage(entity, enemy_entity)
                    entity.attacked = True
                    entity.move = 0
                    if enemy_entity.statistics[Statistics.HitPoints] <= 0:
                        print "enemy destroyed!"
                        if isinstance(enemy_entity, Buildings.Fortress):
                            print "victory!"
                            return True
                        else:
                            Map.SetEmpty(dst_pos)
                    print "succes"
        return False
    
    def Attack(self):
        print "Attack\n"
        if self.army[Geo.NORTH]:
            for x in range(Map.firstQ, Map.thirdQ):
                for y in range(Map.thirdQ, Map.end):
                    if self.EntityAttack(self.nwy, self.nwx, y, x):
                        return True
        if self.army[Geo.SOUTH]:
            for x in range(Map.firstQ, Map.thirdQ):
                for y in range(Map.firstQ):
                    if self.EntityAttack(self.swy, self.swx, y, x):
                        return True
        if self.army[Geo.EAST]:
            for x in range(Map.firstQ):
                for y in range(Map.firstQ, Map.thirdQ):
                    if self.EntityAttack(self.ewy, self.ewx, y, x):
                        return True
        if self.army[Geo.WEST]:
            for x in range(Map.thirdQ, Map.end):
                for y in range(Map.firstQ, Map.thirdQ):
                    if self.EntityAttack(self.wwy, self.wwx, y, x):
                        return True  
        for x in range(Map.end):
            for y in range(Map.end):
                if self.EntityAttack(self.cwy, self.cwx, y, x):
                    return True 
        return False   
                       
    def TakeDamage(self, attacker_unit, enemy_unit):
        print "attacker_unit =", attacker_unit
        print "enemy_unit =", enemy_unit
        print attacker_unit.statistics
        print enemy_unit.statistics
        damage_range = attacker_unit.statistics[Statistics.MaxDamage] - attacker_unit.statistics[Statistics.MinDamage]
        damage = attacker_unit.statistics[Statistics.Attack] * (attacker_unit.statistics[Statistics.MinDamage] + random.randint(0, damage_range))
        print "enemy_unit.hp =",enemy_unit.statistics[Statistics.HitPoints]
        print "damage =",damage
        enemy_unit.statistics[Statistics.HitPoints] -= int(round(float(damage / enemy_unit.statistics[Statistics.Defence])))
        print "enemy_unit.hp =",enemy_unit.statistics[Statistics.HitPoints]
                    
    def FindEnemy(self, pos, unit):
        print "FindEnemy\n"
        attack_range = unit.statistics[Statistics.Range]
        for y_range in range(attack_range + 1):
            for x_range in range(attack_range + 1):
                if unit.army == Geo.NORTH:
                    ny1, nx1 = pos.y + y_range, pos.x + x_range
                    ny2, nx2 = pos.y + y_range, pos.x - x_range
                elif unit.army == Geo.SOUTH:
                    ny1, nx1 = pos.y - y_range, pos.x + x_range
                    ny2, nx2 = pos.y - y_range, pos.x - x_range
                elif unit.army == Geo.EAST:
                    ny1, nx1 = pos.y + y_range, pos.x - x_range
                    ny2, nx2 = pos.y - y_range, pos.x - x_range
                elif unit.army == Geo.WEST:
                    ny1, nx1 = pos.y + y_range, pos.x + x_range
                    ny2, nx2 = pos.y - y_range, pos.x + x_range
                else:
                    ny1, nx1 = pos.y + y_range, pos.x + x_range
                    ny2, nx2 = pos.y - y_range, pos.x + x_range
                    ny3, nx3 = pos.y + y_range, pos.x - x_range
                    ny4, nx4 = pos.y - y_range, pos.x - x_range
                succes, dst_pos = self.CheckEnemy(unit, pos.wy, pos.wx, ny1, nx1)
                if succes:
                    return succes, dst_pos
                succes, dst_pos = self.CheckEnemy(unit, pos.wy, pos.wx, ny2, nx2)
                if succes:
                    return succes, dst_pos
                if unit.army == Geo.CENTRAL:
                    succes, dst_pos = self.CheckEnemy(unit, pos.wy, pos.wx, ny3, nx3)
                    if succes:
                        return succes, dst_pos  
                    succes, dst_pos = self.CheckEnemy(unit, pos.wy, pos.wx, ny4, nx4)
                    if succes:
                        return succes, dst_pos     
        return False, 0
        
    def CheckEnemy(self, unit, wy, wx, y, x):
        dst_pos = Pos(wy, wx, y, x)
        enemy_object = Map.Get(dst_pos)
        if isinstance(enemy_object, Units.Unit) or isinstance(enemy_object, Buildings.Building):
            if enemy_object.owner != unit.owner:
                print "Enemy " + str(enemy_object) + " founded at: " + str(dst_pos.y) + " " + str(dst_pos.x) + "\n"
                return True, dst_pos 
        return False, 0 
    
    def CheckUnit(self, wy, wx, y, x):
        unit = Map.Get(Pos(wy, wx, y, x))
        if isinstance(unit, Units.Unit) and self.attacker == unit.owner:
            return True
        return False
    
    def CheckUnits(self):
        print "CheckUnits\n"
        if self.army[Geo.NORTH]:
            for x in range(Map.firstQ, Map.thirdQ):
                for y in range(Map.thirdQ, Map.end):
                    if self.CheckUnit(self.nwy, self.nwx, y, x):
                        return True
        if self.army[Geo.SOUTH]:
            for x in range(Map.firstQ, Map.thirdQ):
                for y in range(Map.firstQ):
                    if self.CheckUnit(self.swy, self.swx, y, x):
                        return True
        if self.army[Geo.EAST]:
            for x in range(Map.firstQ):
                for y in range(Map.firstQ, Map.thirdQ):
                    if self.CheckUnit(self.ewy, self.ewx, y, x):
                        return True
        if self.army[Geo.WEST]:
            for x in range(Map.thirdQ, Map.end):
                for y in range(Map.firstQ, Map.thirdQ):
                    if self.CheckUnit(self.wwy, self.wwx, y, x):
                        return True
        for x in range(Map.end):
            for y in range(Map.end):
                if self.CheckUnit(self.cwy, self.cwx, y, x):
                    return True
        return False
                
