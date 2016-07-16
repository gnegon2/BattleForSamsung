from collections import OrderedDict
import Control
    
class Resources(OrderedDict):  
    def __init__(self, *arg, **kw):
        super(Resources, self).__init__(*arg, **kw)
        
    def Init(self, gold=0, wood=0, stone=0, crystals=0):
        self[Gold] = gold
        self[Wood] = wood
        self[Stone] = stone
        self[Crystals] = crystals
    
class Gold():
    name = "gold"
    color = Control.CTRL_COLOR_GOLD
    
class Wood():
    name = "wood"
    color = Control.CTRL_COLOR_BROWN
    
class Stone():
    name = "stone"
    color = Control.CTRL_COLOR_STEEL
    
class Crystals():
    name = "crystals"
    color = Control.CTRL_COLOR_VIOLET