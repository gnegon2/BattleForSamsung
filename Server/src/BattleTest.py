from Pos import Pos
import WorldMap
import Units
import Map

def Init(player):
    # Fortress
    if player.username == "test":
        WorldMap.SettleFortress(player, 1, 1)
        Map.Set(player, Units.Peasant, Pos(1, 1, 0, 10))
        
    
    if player.username == "mateusz":
        WorldMap.SettleFortress(player, 0, 1)
        #WorldMap.SettleFortress(player, 2, 1)
        #WorldMap.SettleFortress(player, 1, 0)
        #WorldMap.SettleFortress(player, 1, 2)
    
        # Units
        
        # North
        Map.Set(player, Units.Peasant, Pos(0, 1, 17, 10))
        Map.Set(player, Units.Crossbowman, Pos(0, 1, 18, 13))
        #Map.Set(player, Units.Horseman, Pos(0, 1, 17, 10))
        
        #Map.Set(2, 1,  0,  9, Units.Peasant(player))
        #Map.Set(1, 0,  9, 17, Units.Peasant(player))
        #Map.Set(1, 2,  9,  0, Units.Peasant(player))
