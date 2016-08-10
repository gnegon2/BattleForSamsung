#from Buildings import * # must be
from Data import dbLock
import Data
import pickle
import Config
import Log
import os

class Database():
    
    @staticmethod
    def InitDatabase():
        try:
            Data.mainData.Load(Database.Load())
            Log.Save("Load database.\n")
            return False
        except IOError:
            Log.Save("Init database.\n")
            Data.mainData.Init()  
            return True 
    
    @staticmethod
    def SaveDatabase():
        with dbLock:
            Database.Save(Data.mainData)
            Log.Save("Database saved.\n")
                
    @staticmethod           
    def Save(obj):
        os.system("cp " + Config.databasePath + " ." + Config.databasePath + "_old")
        outputFile = open(Config.databasePath, 'wb')
        pickle.dump(obj, outputFile, -1)
        outputFile.close()
        
    @staticmethod
    def Load(): 
        inputFile = open(Config.databasePath, 'rb')
        obj = pickle.load(inputFile)
        inputFile.close()
        return obj