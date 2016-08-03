from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.shortcuts import print_tokens
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.history import InMemoryHistory
import Commands
import socket
import sys
import getpass
import Config
import Control

class Console():
    history = InMemoryHistory()  
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
        Console.level = int(command[len(Control.CTRL_MENU_UNITS):])
        
    @staticmethod
    def update_complete(data):
        Console.clear_commands()
        commands = Commands.ControlToCommands(data)
        if commands is not Commands.UnitsCommands:
            Console.add_commands(commands)
        else:
            Console.update_level(data)
            Console.add__units_commands()
        if commands is not Commands.MenuCommands:
            Console.add_commands(Commands.MainCommands)
        Console.apply_commands()
            
    @staticmethod
    def clear_commands():
        del Console.commands[:]
        
    @staticmethod
    def add_commands(commands):
        for key, value in sorted(vars(commands).iteritems()):
            if not (key.startswith('__')) and isinstance(value, basestring):
                Console.commands.append(value)
        
    @staticmethod
    def apply_commands():
        Console.commands_completer = WordCompleter(Console.commands, ignore_case=False)
    
    @staticmethod
    def add__units_commands():
        for key, value in sorted(vars(Commands.UnitsCommands).iteritems()):
            if not (key.startswith('__')) and isinstance(value, basestring):
                if value != Commands.UnitsCommands._0_4_MOVE_UNIT:
                    level = int(key[1])
                    if level <= Console.level:
                        Console.commands.append(value)
                else:
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
    ACK = "ACK"   
    maxMsgRcv = 32000
            
    @staticmethod 
    def Read(sock):
        try:
            while True:
                data = sock.recv(Client.maxMsgRcv)
                if data.find(Control.CTRL_EXIT) != -1:
                    print "Closing the game!"
                    sock.sendall(Client.ACK)
                    break
                elif data.find(Control.CTRL_USERNAME) != -1:
                    username = getpass.getuser()
                    sock.sendall(username)
                elif data.find(Control.CTRL_PASSWORD) != -1:
                    text = data[14:]
                    sys.stdout.write(text)
                    pass_msg = prompt(': ', is_password=True)
                    sock.sendall(pass_msg)
                elif data.find(Control.CTRL_INPUT) != -1:
                    msg = prompt(': ', history=Console.history, enable_history_search=True, completer=Console.commands_completer)
                    if msg:  
                        Console.history.append(msg)
                        sock.sendall(msg)
                    else:
                        sock.sendall("NEW_LINE")
                elif data.find(Control.CTRL_MENU) != -1:
                    Console.update_complete(data)
                    sock.sendall(Client.ACK)
                elif data:
                    Console.print_colored(data)
                    sock.sendall(Client.ACK)
                else:
                    print "Server ends connection! Closing the game."
                    break
        except socket.error:
            print "Socket error! Closing the game."
        except KeyboardInterrupt:
            print "User interrupt! Closing the game."
                
    @staticmethod
    def Start(): 
        # Connect the socket to the port where the server is listening
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', Config.port)
        print 'Connecting to %s port %s' % server_address
        try:
            sock.connect(server_address)  
            Client.Read(sock)
        except Exception as e:
            print str(e)
        sock.close()

Client.Start()