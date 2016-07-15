from __future__ import unicode_literals
import socket
import thread
import sys
import getpass

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.shortcuts import print_tokens
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token

import Config
from Control import Control
from Commands import MenuCommands
from Commands import MainCommands
from Commands import WorldMapCommands
from Commands import LocalMapCommands
from Commands import BuildingCommands
from Commands import UnitsCommands
from Commands import ActionCommands
from Commands import BattleCommands
from State import State

class Console():  
    commands = []
    commands_completer = ()
    level = 0
    
    Colors = \
    {
        Token.WHITE: '#FFFFFF',
        Token.RED:   '#FF0000',
        Token.GREEN: '#008000',
        Token.YELLOW:'#FFFF00',
        Token.BLUE:  '#0000FF',
        Token.BROWN: '#964B00',
        Token.GOLD:  '#FFD700',
        Token.VIOLET:'#B803FF',
        Token.STEEL: '#7A7D80',
        Token.AZURE: '#007FFF',
        Token.ORANGE:'#FE7F00',
        Token.WOOD:  '#C04000',
        Token.POPPY: '#E21E13',
        Token.GRANAT:'#000080',
        Token.BLOOD: '#CF2929',  
    }
    
    @staticmethod
    def update_level(command):
        Console.level = int(command[15:])
        
    @staticmethod
    def update_complete():
        Console.clear_commands()
        if Client.state == State.MENU:
            Console.menu_complete()
        elif Client.state == State.BATTLE_MENU:
            Console.battle_menu_complete()
        else:
            if Client.state == State.WORLD_MAP:
                Console.world_map_complete()  
            elif Client.state == State.LOCAL_MAP:
                Console.local_map_complete() 
            elif Client.state == State.BUILDING_MENU:
                Console.building_menu_complete() 
            elif Client.state == State.BUILDING_ACTION_MENU:
                Console.action_menu_complete()
            elif Client.state == State.UNITS_MENU:
                Console.units_menu_complete()
            elif Client.state == State.UNITS_ACTION_MENU:
                Console.action_menu_complete()
            Console.main_complete()
        Console.apply_commands()
    
    @staticmethod
    def clear_commands():
        del Console.commands[:]
        
    @staticmethod
    def apply_commands():
        Console.commands_completer = WordCompleter(Console.commands, ignore_case=False)
    
    @staticmethod
    def menu_complete(): 
        for key, value in vars(MenuCommands).iteritems():
            if not (key.startswith('__')) and isinstance(value, basestring):
                Console.commands.append(value)
        
    @staticmethod
    def main_complete():         
        for key, value in vars(MainCommands).iteritems():
            if not (key.startswith('__')) and isinstance(value, basestring):
                Console.commands.append(value)

    @staticmethod
    def world_map_complete():
        for key, value in vars(WorldMapCommands).iteritems():
            if not (key.startswith('__')) and isinstance(value, basestring):
                Console.commands.append(value)
        
    @staticmethod
    def local_map_complete():
        for key, value in vars(LocalMapCommands).iteritems():
            if not (key.startswith('__')) and isinstance(value, basestring):
                Console.commands.append(value)
    
    @staticmethod
    def building_menu_complete():
        for key, value in vars(BuildingCommands).iteritems():
            if not (key.startswith('__')) and isinstance(value, basestring):
                Console.commands.append(value)
    
    @staticmethod
    def units_menu_complete():
        Console.commands.append(UnitsCommands.MOVE_UNIT)
        Console.commands.append(UnitsCommands.PEASANT)
        if Console.level > 0:
            Console.commands.append(UnitsCommands.ARCHER)
        if Console.level > 1:
            Console.commands.append(UnitsCommands.SWORDMAN)
        if Console.level > 2:
            Console.commands.append(UnitsCommands.PIKEMAN)
        if Console.level > 3:
            Console.commands.append(UnitsCommands.CROSSBOWMAN)
        if Console.level > 4:
            Console.commands.append(UnitsCommands.HORSEMAN)
        if Console.level > 5:
            Console.commands.append(UnitsCommands.CATAPULT)
        if Console.level > 6:
            Console.commands.append(UnitsCommands.CANNON)
            
    @staticmethod
    def action_menu_complete():
        for key, value in vars(ActionCommands).iteritems():
            if not (key.startswith('__')) and isinstance(value, basestring):
                Console.commands.append(value) 
                
    @staticmethod
    def battle_menu_complete(): 
        for key, value in vars(BattleCommands).iteritems():
            if not (key.startswith('__')) and isinstance(value, basestring):
                Console.commands.append(value)
                
    @staticmethod
    def find_color(text):
        pos = text.find(Control.CTRL_COLOR)
        color_len = len(Control.CTRL_COLOR) + 1
        for key, value in vars(Token).items():
            if key.isupper():
                color = text[pos+color_len:pos+color_len+len(key)]
                if key == color:
                    if pos != -1:
                        return pos, color_len+len(key), value
        return -1, -1, -1
    
    @staticmethod   
    def print_colored(text):
        my_style = style_from_dict(Console.Colors)
        tokens = []
        while True:
            pos_start, size, token = Console.find_color(text)
            if pos_start != -1:
                text = text[pos_start+size:]
                pos_end, size, token_end = Console.find_color(text); token_end
                if pos_end != -1:
                    tokens.append((token, text[:pos_end]))
                else:
                    tokens.append((token, text))
                    break
            else:
                break       
        print_tokens(tokens, style=my_style)

class Client:
    'Client class'
    isRunning = True 
    state = State.MENU  
    ACK = "ACK"   
    maxMsgRcv = 32000
            
    @staticmethod 
    def Read(sock):
        try:
            while Client.isRunning:
                data = sock.recv(Client.maxMsgRcv)
                if data.find(Control.CTRL_EXIT) != -1:
                    print "Closing the game!"
                    sock.sendall(Client.ACK)
                    Client.isRunning = False
                elif data.find(Control.CTRL_USERNAME) != -1:
                    username = getpass.getuser()
                    sock.sendall(username)
                elif data.find(Control.CTRL_PASSWORD) != -1:
                    text = data[14:]
                    sys.stdout.write(text)
                    pass_msg = prompt(': ', is_password=True)
                    sock.sendall(pass_msg)
                elif data.find(Control.CTRL_INPUT) != -1:
                    msg = prompt(': ', completer=Console.commands_completer)
                    sock.sendall(msg)
                elif data.find(Control.CTRL_MENU) != -1:
                    Client.state = State.MENU
                    Console.update_complete()
                    sock.sendall(Client.ACK)
                elif data.find(Control.CTRL_WORLD_MAP) != -1:
                    Client.state = State.WORLD_MAP
                    Console.update_complete()
                    sock.sendall(Client.ACK)
                elif data.find(Control.CTRL_SCOUTING_MODE) != -1:
                    Client.state = State.SCOUTING_MODE
                    Console.update_complete()
                    sock.sendall(Client.ACK)
                elif data.find(Control.CTRL_LOCAL_MAP) != -1:
                    Client.state = State.LOCAL_MAP
                    Console.update_complete()
                    sock.sendall(Client.ACK)
                elif data.find(Control.CTRL_BUILDING_MENU) != -1:
                    Client.state = State.BUILDING_MENU
                    Console.update_complete()
                    sock.sendall(Client.ACK)
                elif data.find(Control.CTRL_BUILDING_ACTION_MENU) != -1:
                    Client.state = State.BUILDING_ACTION_MENU
                    Console.update_complete()
                    sock.sendall(Client.ACK)
                elif data.find(Control.CTRL_UNITS_MENU) != -1:
                    Client.state = State.UNITS_MENU
                    Console.update_level(data)
                    Console.update_complete()
                    sock.sendall(Client.ACK)
                elif data.find(Control.CTRL_UNITS_ACTION_MENU) != -1:
                    Client.state = State.UNITS_ACTION_MENU
                    Console.update_complete()
                    sock.sendall(Client.ACK)
                elif data.find(Control.CTRL_BATTLE_MENU) != -1:
                    Client.state = State.BATTLE_MENU
                    Console.update_complete()
                    sock.sendall(Client.ACK)
                elif data:
                    if data.find(Control.CTRL_COLOR) != -1:
                        Console.print_colored(data)
                    else:
                        sys.stdout.write(data)
                    sock.sendall(Client.ACK)
                else:
                    print "Server ends connection! Closing the game."
                    Client.isRunning = False 
        except socket.error:
            print "Server ends connection! Closing the game."
            Client.isRunning = False
        except KeyboardInterrupt:
            print "User interrupt! Closing the game."
            Client.isRunning = False
                
    @staticmethod
    def Start(): 
        # Connect the socket to the port where the server is listening
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', Config.port)
        print 'Connecting to %s port %s' % server_address
        try:
            sock.connect(server_address)  
            thread.start_new_thread(Client.Read, (sock,) )
            while Client.isRunning:
                pass
            sock.close()
        except:
            sock.close()

Client.Start()