from Data import mainData
from Data import dbLock
import Log
import Control
import Crypt
 
maxMsgResponse = 255
 
def SendMsg(player, data, response = False):
    player.connection.sendall(data)
    if response:
        player.connection.recv(maxMsgResponse)
        player.connection.sendall(Control.CTRL_INPUT)
    return player.connection.recv(maxMsgResponse)

def CheckUserName(username):
    Log.Save("Checking username: " + username + "\n")
    with dbLock:
        for username_arg, password_arg in mainData.users:
            password_arg
            if username_arg == username:
                return True
        return False

def CheckPassword(username, password):
    Log.Save("Checking password for username: " + username + "\n")
    with dbLock:
        for username_arg, password_arg in mainData.users:
            if username_arg == username:
                decrypted_password = Crypt.Decrypt(password_arg, password)
                if decrypted_password == password:
                    return True
                else:
                    return False

def CreateAccount(username, password):
    Log.Save("Creating account for username: " + username)
    account = (username, Crypt.Encrypt(password, password))
    with dbLock:
        mainData.users.append(account)  
    
def ResetPassword(username):
    Log.Save("Reseting password for username: " + username)
    with dbLock:    
        for username_arg, password_arg in mainData.users:
            password_arg
            if username_arg == username:
                mainData.users.remove((username,password_arg))