from WorldMap import WorldMap
from LocalMapStruct import localMaps
from Units import Units

def Init(player):
    # Fortress
    WorldMap.SettleFortress(player, 1, 1)
    
    WorldMap.SettleFortress(player, 0, 1)
    WorldMap.SettleFortress(player, 2, 1)
    WorldMap.SettleFortress(player, 1, 0)
    WorldMap.SettleFortress(player, 1, 2)
    
    # Units
    
    # North
    localMaps[0][1].fields[19][10] = Units.Peasant(player)
    localMaps[0][1].fields[18][9] = Units.Peasant(player)
    localMaps[0][1].fields[17][8] = Units.Peasant(player)
    
    
    localMaps[2][1].fields[0][9] = Units.Peasant(player)
    localMaps[1][0].fields[9][17] = Units.Peasant(player)
    localMaps[1][2].fields[9][0] = Units.Peasant(player)