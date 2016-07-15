from Crypt import Crypt
from Log import Log
from Control import Control
from Data import Data

class Utility():   
    maxMsgResponse = 255
     
    @staticmethod
    def SendMsg(player, data, response = False):
        player.connection.sendall(data)
        if response:
            player.connection.recv(Utility.maxMsgResponse)
            player.connection.sendall(Control.CTRL_INPUT)
        return player.connection.recv(Utility.maxMsgResponse)
    
    @staticmethod
    def CheckUserName(username):
        Log.Save("Checking username: " + username)
        for username_arg, password_arg in Data.users:
            password_arg
            if username_arg == username:
                return True
        return False
    
    @staticmethod
    def CheckPassword(username, password):
        Log.Save("Checking password for username: " + username)
        for username_arg, password_arg in Data.users:
            if username_arg == username:
                decrypted_password = Crypt.Decrypt(password_arg, password)
                if decrypted_password == password:
                    return True
                else:
                    return False
    
    @staticmethod
    def CreateAccount(username, password):
        Log.Save("Creating account for username: " + username)
        account = (username, Crypt.Encrypt(password, password))
        Data.users.append(account)  
        
    @staticmethod
    def ResetPassword(username):
        Log.Save("Reseting password for username: " + username)
        for username_arg, password_arg in Data.users:
            password_arg
            if username_arg == username:
                Data.users.remove((username,password_arg))