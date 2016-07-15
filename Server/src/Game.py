from Log import Log
from WorldMap import WorldMap
from LocalMap import LocalMap
from Player import State
from Control import Control
from Utility import Utility 
from Commands import MenuCommands, MainCommands
from Commands import WorldMapCommands
from Commands import LocalMapCommands

class Game():
    @staticmethod
    def InitGame():
        Log.Init()
        WorldMap.LoadMap()
        WorldMap.InitLocalMaps()
        WorldMap.InitForbiddenPlaces()
            
    @staticmethod
    def MainMenu(player):
        Log.Save("New player enter main menu!\n")
        Utility.SendMsg(player, Control.CTRL_MENU)
        menu =  Control.CTRL_COLOR_AZURE
        menu += "Welcome in Battle For Samsung game!\n"
        menu += "choose one of the available options:\n"
        Utility.SendMsg(player, menu)
        Utility.SendMsg(player, MenuCommands.Get())
        
        while player.state != State.EXITING:
            reply = Utility.SendMsg(player, Control.CTRL_INPUT)
            Log.Save("Player reply is: " + reply + "\n")
            if reply == MenuCommands.REGISTER:
                Game.Register(player)
                break
            elif reply == MenuCommands.LOGIN:
                Game.Login(player)
                break
            elif reply == MenuCommands.EXIT:
                Game.Exit(player)
            else:
                Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Undefined option!\n")
    
    @staticmethod
    def Register(player):
        #=======================================================================
        # registerMsg = Control.CTRL_COLOR_AZURE
        # registerMsg += "In order to create new account\n"
        # registerMsg += "please enter user name:\n"
        # 
        # player.username = Utility.SendMsg(player, registerMsg, True)
        # 
        # while Utility.CheckUserName(player.username):
        #     errorMsg = Control.CTRL_COLOR_RED
        #     errorMsg +=  "Username "
        #     errorMsg += player.username
        #     errorMsg += " already exist!\n"
        #     errorMsg += "Enter another user name:\n"
        #     
        #     player.username = Utility.SendMsg(player, errorMsg, True)
        #=======================================================================
        
        player.username = Utility.SendMsg(player, Control.CTRL_USERNAME)
        
        if Utility.CheckUserName(player.username):
            errorMsg = Control.CTRL_COLOR_RED
            errorMsg +=  "Username "
            errorMsg += player.username
            errorMsg += " already exist!\n"
            
            Utility.SendMsg(player, errorMsg)
            return
        
        Utility.SendMsg(player, Control.CTRL_COLOR_AZURE + "please enter password:\n") 
        password = Utility.SendMsg(player, Control.CTRL_PASSWORD) 
        
        Utility.CreateAccount(player.username, password)
        Utility.SendMsg(player, Control.CTRL_COLOR_GREEN +  "Account successfully created!\n")
        
        player.loggedIn = True
        player.state = State.WORLD_MAP
        player.InitResources()
        player.InitUserInfo()
        Log.Save("New account created: " + player.username + "\n");
        
    @staticmethod
    def Login(player):    
    #===========================================================================
    #     player.username = Utility.SendMsg(player, Control.CTRL_COLOR_AZURE + "In order to login\nplease enter user name:\n", True)
    # 
    #     while not Utility.CheckUserName(player.username):
    #         errorMsg = Control.CTRL_COLOR_RED
    #         errorMsg +=  "Username "
    #         errorMsg += player.username
    #         errorMsg += " doesn't exist!\n"
    #         errorMsg += "Enter correct user name:\n"
    # 
    #         player.username = Utility.SendMsg(player, errorMsg, True)
    #===========================================================================
    
        player.username = Utility.SendMsg(player, Control.CTRL_USERNAME)
        
        if not Utility.CheckUserName(player.username):
            errorMsg = Control.CTRL_COLOR_RED
            errorMsg +=  "Username "
            errorMsg += player.username
            errorMsg += " doesn't exist!\n"
     
            Utility.SendMsg(player, errorMsg)
            return

        Utility.SendMsg(player, Control.CTRL_COLOR_AZURE + "please enter password:\n") 
        password = Utility.SendMsg(player, Control.CTRL_PASSWORD)
    
        while not Utility.CheckPassword(player.username, password):
            Utility.SendMsg(player, Control.CTRL_COLOR_RED + "Wrong password!\nPlease enter correct password:\n")
            password = Utility.SendMsg(player, Control.CTRL_PASSWORD)
    
        Utility.SendMsg(player, Control.CTRL_COLOR_GREEN + "Successfully logged in!\n")
    
        player.loggedIn = True
        player.state = State.WORLD_MAP
        player.LoadResources()
        player.LoadUserInfo()
        Log.Save("New player logged in: " + player.username + "\n")  
    
    @staticmethod
    def Exit(player):
        Utility.SendMsg(player, Control.CTRL_EXIT)
        player.connection.close()
        player.state = State.EXITING
        Log.Save("Player exits the game!\n")
        
    @staticmethod
    def WorldMap(player):
        Log.Save(player.username + " enters World Map\n")
        
        worldMapMenu =  Control.CTRL_COLOR_AZURE
        worldMapMenu +=  "Welcome on World Map!\n"
        worldMapMenu += "choose one of the available options:\n"
        Utility.SendMsg(player, worldMapMenu)
        Utility.SendMsg(player, WorldMapCommands.Get())
        Utility.SendMsg(player, MainCommands.Get())
        
        while player.state == State.WORLD_MAP:
            Utility.SendMsg(player, Control.CTRL_WORLD_MAP)
            command = Utility.SendMsg(player, Control.CTRL_INPUT)
            WorldMap.ExecuteCommand(player, command)   
            
    @staticmethod
    def LocalMap(player):
        Log.Save(player.username + " enters Local Map\n")
        
        localMapMenu =  Control.CTRL_COLOR_AZURE
        localMapMenu +=  "Welcome on Local Map!\n"
        localMapMenu += "choose one of the available options:\n"
        Utility.SendMsg(player, localMapMenu)
        Utility.SendMsg(player, LocalMapCommands.Get())
        Utility.SendMsg(player, MainCommands.Get())
        
        while player.state == State.LOCAL_MAP:
            Utility.SendMsg(player, Control.CTRL_LOCAL_MAP)
            command = Utility.SendMsg(player, Control.CTRL_INPUT)
            LocalMap.ExecuteCommand(player, command)  