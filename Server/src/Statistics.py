from collections import OrderedDict
from Colors import Colors

class Statistics(OrderedDict):  
    def __init__(self, *arg, **kw):
        super(Statistics, self).__init__(*arg, **kw)
        
    def Init(self, hit_points=0, defence=0, attack=0, min_damage=0, max_damage=0, attack_range=0, speed=0):
        self[HitPoints] = hit_points
        self[Defence] = defence
        self[Attack] = attack
        self[MinDamage] = min_damage
        self[MaxDamage] = max_damage
        self[Range] = attack_range
        self[Speed] = speed
    
class HitPoints():
    name = "hit points"
    color = Colors.COLOR_GREEN
    
class Defence():
    name = "defence"
    color = Colors.COLOR_STEEL
    
class Attack():
    name = "attack"
    color = Colors.COLOR_RED
    
class MinDamage():
    name = "min damage"
    color = Colors.COLOR_BROWN
    
class MaxDamage():
    name = "max damage"
    color = Colors.COLOR_VIOLET
    
class Range():
    name = "range"
    color = Colors.COLOR_GOLD
    
class Speed():
    name = "speed"
    color = Colors.COLOR_AZURE