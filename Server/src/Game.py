from Commands import MenuCommands, MainCommands, LocalMapCommands, WorldMapCommands
from Colors import Colors
from Data import mainData
from Database import Database
from Map import mainMap as Map
import Log
import WorldMap
import LocalMap
import State
import Control
import Utility 
import Commands
import Buildings

def InitGame():
    Log.Init()
    if Database.InitDatabase():
        WorldMap.LoadMap()
        WorldMap.InitForbiddenPlaces()
        mainData.map = Map
        Database.SaveDatabase()
    else:
        WorldMap.LoadMapFromDb()
    Buildings.InitFortressLevels()

def MainMenu(player):
    Log.Save("New player enter main menu!\n")
    menu =  Colors.COLOR_AZURE
    menu += "Welcome in Battle For Samsung game!\n"
    menu += "choose one of the available options:\n"
    Utility.SendMsg(player, menu)
    Utility.SendMsg(player, Control.CTRL_MENU_MAIN)
    Utility.SendMsg(player, Commands.GetCommands(MenuCommands))
    
    while player.state != State.EXITING:
        reply = Utility.SendMsg(player, Control.CTRL_INPUT)
        Log.Save("Player reply is: " + reply + "\n")
        if reply == MenuCommands._0_0_REGISTER:
            Register(player)
            break
        elif reply == MenuCommands._1_0_LOGIN:
            Login(player)
            break
        elif reply == MenuCommands._2_0_EXIT:
            Exit(player)
        else:
            Utility.SendMsg(player, Colors.COLOR_RED + "Undefined option!\n")

def Register(player):  
    player.username = Utility.SendMsg(player, Control.CTRL_USERNAME)
    
    if Utility.CheckUserName(player.username):
        errorMsg = Colors.COLOR_RED
        errorMsg +=  "Username "
        errorMsg += player.username
        errorMsg += " already exist!\n"
        
        Utility.SendMsg(player, errorMsg)
        return
    
    Utility.SendMsg(player, Colors.COLOR_AZURE + "please enter password:\n") 
    password = Utility.SendMsg(player, Control.CTRL_PASSWORD) 
    
    Utility.CreateAccount(player.username, password)
    Utility.SendMsg(player, Colors.COLOR_GREEN +  "Account successfully created!\n")
    
    player.loggedIn = True
    player.state = State.WORLD_MAP
    player.InitResources()
    player.InitUserInfo()
    Log.Save("New account created: " + player.username + "\n");

def Login(player):     
    player.username = Utility.SendMsg(player, Control.CTRL_USERNAME)
    
    if not Utility.CheckUserName(player.username):
        errorMsg = Colors.COLOR_RED
        errorMsg +=  "Username "
        errorMsg += player.username
        errorMsg += " doesn't exist!\n"
 
        Utility.SendMsg(player, errorMsg)
        return

    Utility.SendMsg(player, Colors.COLOR_AZURE + "please enter password:\n") 
    password = Utility.SendMsg(player, Control.CTRL_PASSWORD)

    while not Utility.CheckPassword(player.username, password):
        Utility.SendMsg(player, Colors.COLOR_RED + "Wrong password!\nPlease enter correct password:\n")
        password = Utility.SendMsg(player, Control.CTRL_PASSWORD)

    Utility.SendMsg(player, Colors.COLOR_GREEN + "Successfully logged in!\n")

    player.loggedIn = True
    player.state = State.WORLD_MAP
    player.LoadResources()
    player.LoadUserInfo()
    Log.Save("New player logged in: " + player.username + "\n")  

def Exit(player):
    Utility.SendMsg(player, Control.CTRL_EXIT)
    player.connection.close()
    player.state = State.EXITING
    Log.Save("Player exits the game!\n")

def WorldMapMenu(player):
    Log.Save(player.username + " enters World Map\n")
    
    worldMapMenu =  Colors.COLOR_AZURE
    worldMapMenu +=  "Welcome on World Map!\n"
    worldMapMenu += "choose one of the available options:\n"
    Utility.SendMsg(player, worldMapMenu)
    Utility.SendMsg(player, Commands.GetCommands(WorldMapCommands))
    Utility.SendMsg(player, Commands.GetCommands(MainCommands))
    
    while player.state == State.WORLD_MAP:
        Utility.SendMsg(player, Control.CTRL_MENU_WORLD_MAP)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        Log.Save(player.username + " enter command: " + command + "\n")
        WorldMap.ExecuteCommand(player, command)   

def LocalMapMenu(player):
    Log.Save(player.username + " enters Local Map\n")
    
    localMapMenu =  Colors.COLOR_AZURE
    localMapMenu +=  "Welcome on Local Map!\n"
    localMapMenu += "choose one of the available options:\n"
    Utility.SendMsg(player, localMapMenu)
    Utility.SendMsg(player, Commands.GetCommands(LocalMapCommands))
    Utility.SendMsg(player, Commands.GetCommands(MainCommands))
    
    while player.state == State.LOCAL_MAP:
        Utility.SendMsg(player, Control.CTRL_MENU_LOCAL_MAP)
        command = Utility.SendMsg(player, Control.CTRL_INPUT)
        Log.Save(player.username + " enter command: " + command + "\n")
        fort = Map.GetFort(player.wy, player.wx) 
        if fort is not None and fort.owner == player.username:
            LocalMap.ExecuteCommand(player, command)
        else:
            player.state = State.WORLD_MAP
            Utility.SendMsg(player, "Fortress overtaken!\n Returning to World Map!\n")  