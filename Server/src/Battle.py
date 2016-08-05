from Map import mainMap as Map
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
    
    def Start(self, player):
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
            self.Attack(player)
            while True:
                if not self.AttackerMove():
                    break
            self.Attack(player)
            
            if not self.CheckUnits():
                return False
            if not self.CheckFortress():
                return True
     
    def InitEntity(self, wy, wx, y, x, geo):
        entity = Map.Get(Pos(wy, wx, y, x))
        if isinstance(entity, Units.Unit) or isinstance(entity, Buildings.Building):
            entity.army = geo
                      
    def InitBattle(self):
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
        if isinstance(unit, Units.Unit) and unit.owner == self.attacker.username and unit.move > 0:
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
        if isinstance(unit, Units.Unit) and unit.owner == self.attacker.username:
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
    
    def EntityAttack(self, player, wy, wx, y, x):
        src_pos = Pos(wy, wx, y, x)
        entity = Map.Get(src_pos)  
        if (isinstance(entity, Units.Unit) or isinstance(entity, Buildings.Building)) and not entity.attacked:
            attack_range = entity.statistics[Statistics.Range]
            if attack_range > 0:
                succes, dst_pos = self.FindEnemy(src_pos, entity)
                if succes:
                    enemy_entity = Map.Get(dst_pos)
                    self.TakeDamage(player, entity, enemy_entity)
                    entity.attacked = True
                    entity.move = 0
                    if enemy_entity.statistics[Statistics.HitPoints] <= 0:
                        if self.log:
                            if entity.owner == self.attacker.username:
                                Utility.SendMsg(player, Colors.COLOR_GREEN + "Entity " + enemy_entity.__class__.__name__ + " destroyed!\n")
                            else:
                                Utility.SendMsg(player, Colors.COLOR_RED + "Your unit " + enemy_entity.__class__.__name__ + " destroyed!\n")
                        Map.SetEmpty(dst_pos)
    
    def Attack(self, player):
        if self.army[Geo.NORTH]:
            for x in range(Map.firstQ, Map.thirdQ):
                for y in range(Map.thirdQ, Map.end):
                    self.EntityAttack(player, self.nwy, self.nwx, y, x)
        if self.army[Geo.SOUTH]:
            for x in range(Map.firstQ, Map.thirdQ):
                for y in range(Map.firstQ):
                    self.EntityAttack(player, self.swy, self.swx, y, x)
        if self.army[Geo.EAST]:
            for x in range(Map.firstQ):
                for y in range(Map.firstQ, Map.thirdQ):
                    self.EntityAttack(player, self.ewy, self.ewx, y, x)
        if self.army[Geo.WEST]:
            for x in range(Map.thirdQ, Map.end):
                for y in range(Map.firstQ, Map.thirdQ):
                    self.EntityAttack(player, self.wwy, self.wwx, y, x) 
        for x in range(Map.end):
            for y in range(Map.end):
                self.EntityAttack(player, self.cwy, self.cwx, y, x) 
    
    def Weaknesses(self, attacker, defender):
        if attacker == Units.Horseman and defender == Units.Pikeman:
            return -0.5
        elif attacker == Units.Pikeman and defender == Units.Horseman:
            return 0.5
        elif (attacker == Units.Archer or attacker == Units.Crossbowman) and (defender == Units.Swordman or defender == Units.Pikeman):
            return -0.3
        elif (attacker == Units.Swordman or attacker == Units.Pikeman) and (defender == Units.Archer or defender == Units.Crossbowman):
            return 0.7
        elif attacker == Units.Catapult and isinstance(defender, Buildings.Building):
            return 0.6
        elif attacker == Units.Cannon and isinstance(defender, Buildings.Building):
            return 0.3
        return 0
                      
    def TakeDamage(self, player, attacker_unit, enemy_unit):
        print "attacker_unit =", attacker_unit
        print "enemy_unit =", enemy_unit
        damage_range = attacker_unit.statistics[Statistics.MaxDamage] - attacker_unit.statistics[Statistics.MinDamage]
        power = attacker_unit.statistics[Statistics.Attack] * (attacker_unit.statistics[Statistics.MinDamage] + random.randint(0, damage_range))
        power = int(power  + power * self.Weaknesses(attacker_unit, enemy_unit))
        print "enemy_unit.hp =",enemy_unit.statistics[Statistics.HitPoints]
        print "power =",power
        damage = int(round(float(power / enemy_unit.statistics[Statistics.Defence])))
        if damage < 1:
            damage = 1
        print "damage =",damage
        enemy_unit.statistics[Statistics.HitPoints] -= damage
        print "enemy_unit.hp =",enemy_unit.statistics[Statistics.HitPoints]
        if self.log:
            if attacker_unit.owner == self.attacker.username:
                Utility.SendMsg(player, Colors.COLOR_GREEN + "Your " + attacker_unit.__class__.__name__ + " attack " + enemy_unit.__class__.__name__ + " taking " + str(damage) + " damage!\n")
            else:
                Utility.SendMsg(player, Colors.COLOR_RED + "Enemy unit " + attacker_unit.__class__.__name__ + " attack your " +  enemy_unit.__class__.__name__ + " taking " + str(damage) + " damage!\n")
                    
    def FindEnemy(self, pos, unit):
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
                return True, dst_pos 
        return False, 0 
    
    def CheckUnit(self, wy, wx, y, x):
        unit = Map.Get(Pos(wy, wx, y, x))
        if isinstance(unit, Units.Unit) and self.attacker.username == unit.owner:
            return True
        return False
    
    def CheckUnits(self):
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
                
    def CheckFortress(self):
        fort = Map.GetFort(self.cwy, self.cwx)
        if fort is None:
            return False
        return True
        