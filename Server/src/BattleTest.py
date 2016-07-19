from Pos import Pos
import Buildings
import WorldMap
import Units
import Map

def Init(player):
    # Fortress
    if player.username == "test":
        WorldMap.SettleFortress(player, 1, 1)
        Map.Set(player, Units.Peasant, Pos(1, 1, 0, 10))
        
    
    if player.username == "k.kaganiec":
        WorldMap.SettleFortress(player, 0, 1)
        #=======================================================================
        # WorldMap.SettleFortress(player, 2, 1)
        # WorldMap.SettleFortress(player, 1, 0)
        # WorldMap.SettleFortress(player, 1, 2)
        #=======================================================================
    
        player.wy = 0
        player.wx = 1
        
        #=======================================================================
        # Map.Set(player, Buildings.Library, Pos(0,1,8,8) )
        # Map.Set(player, Buildings.Library, Pos(0,1,8,9) )
        # Map.Set(player, Buildings.Library, Pos(0,1,8,10) )
        # Map.Set(player, Buildings.Library, Pos(0,1,8,11) )
        # Map.Set(player, Buildings.Library, Pos(0,1,8,12) )
        # 
        # player.wy = 2
        # player.wx = 1
        # 
        # Map.Set(player, Buildings.Library, Pos(2,1,8,8) )
        # Map.Set(player, Buildings.Library, Pos(2,1,8,9) )
        # Map.Set(player, Buildings.Library, Pos(2,1,8,10) )
        # Map.Set(player, Buildings.Library, Pos(2,1,8,11) )
        # 
        # player.wy = 1
        # player.wx = 0
        # 
        # Map.Set(player, Buildings.Library, Pos(1,0,8,8) )
        # Map.Set(player, Buildings.Library, Pos(1,0,8,9) )
        # Map.Set(player, Buildings.Library, Pos(1,0,8,10) )
        # 
        # player.wy = 1
        # player.wx = 2
        # 
        # Map.Set(player, Buildings.Library, Pos(1,2,8,8) )
        # Map.Set(player, Buildings.Library, Pos(1,2,8,9) )
        #=======================================================================
        
        # Units
        
        # North
        Map.Set(player, Units.Peasant, Pos(0, 1, 17, 10))
        Map.Set(player, Units.Crossbowman, Pos(0, 1, 18, 13))
        Map.Set(player, Units.Horseman, Pos(0, 1, 19, 11))
        
        #=======================================================================
        # # South
        # Map.Set(player, Units.Peasant, Pos(2, 1, 0, 10))
        # Map.Set(player, Units.Crossbowman, Pos(2, 1, 1, 13))
        # Map.Set(player, Units.Horseman, Pos(2, 1, 2, 11))
        # 
        # # East
        # Map.Set(player, Units.Peasant, Pos(1, 2, 10, 0))
        # Map.Set(player, Units.Crossbowman, Pos(1, 2, 9, 0))
        # Map.Set(player, Units.Horseman, Pos(1, 2, 11, 1))
        # 
        # # West
        # Map.Set(player, Units.Peasant, Pos(1, 0, 10, 18))
        # Map.Set(player, Units.Crossbowman, Pos(1, 0, 11, 19))
        # Map.Set(player, Units.Horseman, Pos(1, 0, 9, 17))
        #=======================================================================
        
    if player.username == "m.grzegorzek":
        WorldMap.SettleFortress(player, 1, 1) 
        
        player.wy = 1
        player.wx = 1
        
        #=======================================================================
        # Map.Set(player, Buildings.Tower, Pos(1,1,14,5) )
        # Map.Set(player, Buildings.Tower, Pos(1,1,14,15) )
        # Map.Set(player, Buildings.Tower, Pos(1,1,5,5) )
        # Map.Set(player, Buildings.Tower, Pos(1,1,5,14) )
        #=======================================================================
        
        Map.Set(player, Buildings.Library, Pos(1,1,8,8) )
        Map.Set(player, Buildings.Library, Pos(1,1,8,9) )
        Map.Set(player, Buildings.Library, Pos(1,1,8,10) )
        Map.Set(player, Buildings.Library, Pos(1,1,8,11) )
        
        #=======================================================================
        # Map.Set(player, Units.Horseman, Pos(1, 1, 14, 6))
        # Map.Set(player, Units.Horseman, Pos(1, 1, 14, 14))
        # Map.Set(player, Units.Horseman, Pos(1, 1, 5, 6))
        # Map.Set(player, Units.Horseman, Pos(1, 1, 5, 13))
        #=======================================================================
        
        #=======================================================================
        # Map.Set(player, Units.Catapult, Pos(1, 1, 14, 7))
        #=======================================================================
        Map.Set(player, Units.Catapult, Pos(1, 1, 5, 7))
        
