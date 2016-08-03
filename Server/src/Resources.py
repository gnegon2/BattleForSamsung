from collections import OrderedDict
from Colors import Colors
    
class Resources(OrderedDict):  
    def __init__(self, *arg, **kw):
        super(Resources, self).__init__(*arg, **kw)
        
    def Init(self, gold=0, wood=0, stone=0, crystals=0, science=0):
        self[Gold] = gold
        self[Wood] = wood
        self[Stone] = stone
        self[Crystals] = crystals
        self[Science] = science
    
class Gold():
    name = "gold"
    color = Colors.COLOR_GOLD
    
class Wood():
    name = "wood"
    color = Colors.COLOR_BROWN
    
class Stone():
    name = "stone"
    color = Colors.COLOR_STEEL
    
class Crystals():
    name = "crystals"
    color = Colors.COLOR_VIOLET
    
class Science():
    name = "science"
    color = Colors.COLOR_AZURE