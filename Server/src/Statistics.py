from collections import OrderedDict
import Control

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
    color = Control.CTRL_COLOR_GREEN
    
class Defence():
    name = "defence"
    color = Control.CTRL_COLOR_STEEL
    
class Attack():
    name = "attack"
    color = Control.CTRL_COLOR_RED
    
class MinDamage():
    name = "min damage"
    color = Control.CTRL_COLOR_BROWN
    
class MaxDamage():
    name = "max damage"
    color = Control.CTRL_COLOR_VIOLET
    
class Range():
    name = "range"
    color = Control.CTRL_COLOR_GOLD
    
class Speed():
    name = "speed"
    color = Control.CTRL_COLOR_AZURE