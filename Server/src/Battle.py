from BattleMap import BattleMap
from LocalMapStruct import localMaps
import Config
from Log import Log
from Control import Type
from Buildings import Buildings
from Utility import Utility
from Commands import BattleCommands
from Control import Control

class Battle():
    
    def __init__(self, attacker, defender, army, worldPosY, worldPosX):
        Log.Save("Init battle on field: "+ str(worldPosY) + " " + str(worldPosX) + "!\n")
        self.attacker = attacker
        self.defender = defender
        self.army = army
        self.worldPosY = worldPosY
        self.worldPosX = worldPosX
    
    def Start(self):
        Log.Save("Start battle on field: "+ str(self.worldPosY) + " " + str(self.worldPosX) + "!\n")
        battleMap = BattleMap(self.attacker, self.army, self.worldPosY, self.worldPosX)
        
        battleMenu = Control.CTRL_COLOR_AZURE
        battleMenu += "Welcome in Battle Menu!\n"
        battleMenu += "available options are:\n"
        Utility.SendMsg(self.attacker, battleMenu)
        Utility.SendMsg(self.attacker, BattleCommands.Get())
        
        Utility.SendMsg(self.attacker, Control.CTRL_BATTLE_MENU)
        command = Utility.SendMsg(self.attacker, Control.CTRL_INPUT)

        while True:
            if command == BattleCommands.MAKE_MOVE:
                battleMap.ShowBattleMap()
                command = Utility.SendMsg(self.attacker, Control.CTRL_INPUT)
            if self.army['OnNorth']:
                self.AttackerNorthMove()

        
    def AttackerNorthMove(self):
        localMapStruct = localMaps[self.worldPosY][self.worldPosX]
        print "Moving army on north"
        localMapStructNorth = localMaps[self.worldPosY - 1][self.worldPosX]
        for x in range(Config.localMapSize / 4, 3 * Config.localMapSize / 4):
            y = 3 * Config.localMapSize / 4
            while y < Config.localMapSize:
                instance = localMapStructNorth.fields[y][x]
                if instance.type == Type.UNIT:       
                    print "instance = " + str(instance)
                    print y, x
                    y_instance = y
                    movedToNextMap = False
                    for y_move in range(instance.speed):
                        print "y_instance = " + str(y_instance)
                        next_field = y_instance + 1
                        if next_field < Config.localMapSize:
                            destInstance = localMapStructNorth.fields[next_field][x]
                            print "destInstance = " + str(destInstance)
                            if isinstance(destInstance, Buildings.Empty):
                                print "Movin!"
                                instance.moved = True
                                localMapStructNorth.fields[next_field][x] = instance
                                localMapStructNorth.fields[y_instance][x] = Buildings.Empty()
                                y_instance += 1
                                y += 1 
                            else:
                                break
                        else:
                            destInstance = localMapStruct.fields[0][x]
                            if isinstance(destInstance, Buildings.Empty):
                                print "Movin!"
                                instance.moved = True
                                localMapStruct.fields[0][x] = instance
                                localMapStructNorth.fields[y_instance][x] = Buildings.Empty()
                                y_instance = 0
                                if y_move < instance.speed - 1:
                                    movedToNextMap = True
                    if movedToNextMap:
                        y_instance = 0
                        for y_move in range(Config.localMapSize - y - 2 + instance.speed):
                            next_field = y_instance + 1
                            destInstance = localMapStruct.fields[next_field][x]
                            print "destInstance = " + str(destInstance)
                            if isinstance(destInstance, Buildings.Empty):
                                print "Movin!"
                                localMapStruct.fields[next_field][x] = instance
                                localMapStruct.fields[y_instance][x] = Buildings.Empty()
                                y_instance += 1
                                y += 1 
                            else:
                                break
                y += 1            
                    
        
        