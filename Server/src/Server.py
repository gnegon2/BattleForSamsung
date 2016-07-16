from Player import Player
import socket
import thread
import Config
import State
import Log
import Game

import BattleTest

def Session(connection, client_address):
    Log.Save("New player connected!\n") 
    try:
        player = Player(connection)
        initialize = False
        while player.state != State.EXITING:
            if player.state == State.INIT:
                Game.MainMenu(player)
            if player.loggedIn:
                if not initialize:
                    BattleTest.Init(player)
                    initialize = True
                if player.state == State.WORLD_MAP:
                    Game.WorldMapMenu(player)
                elif player.state == State.LOCAL_MAP:
                    Game.LocalMapMenu(player)
                    
        Log.Save(player.username + " exits the game!\n")        
            
    except socket.error:
        Log.Save("Client end connection!\n")
    except Exception as inst:
        Log.Save(inst.__str__())
        Log.Save("Server close connection!\n")
     
def Start():
    Game.InitGame()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', Config.port)
    sock.bind(server_address)
    sock.listen(5)
    Log.Save("Starting up server.\n")
    while True:
        # Wait for a connection
        Log.Save("Waiting for a connection...\n")
        try:
            connection, client_address = sock.accept()
            thread.start_new_thread( Session, (connection, client_address, ) )
        except:
            Log.Save("Error. Stopping Server.")
            break
    sock.close()  
         
Start()
    