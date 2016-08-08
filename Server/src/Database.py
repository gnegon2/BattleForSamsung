#from Buildings import * # must be
from Data import dbLock
import Data
import pickle
import Config
import Log

class Database():
    
    @staticmethod
    def InitDatabase():
        Log.Save("Init database.\n")
        Data.mainData.Init()
        
    @staticmethod
    def LoadDatabase(): 
        Log.Save("Load database.\n") 
        Data.mainData.Load(Database.Load()) 
    
    @staticmethod
    def SaveDatabase():
        with dbLock:
            Database.Save(Data.mainData)
            Log.Save("Database saved.\n")
                
    @staticmethod           
    def Save(obj):
        outputFile = open(Config.databasePath, 'wb')
        pickle.dump(obj, outputFile, -1)
        outputFile.close()
        
    @staticmethod
    def Load(): 
        inputFile = open(Config.databasePath, 'rb')
        obj = pickle.load(inputFile)
        inputFile.close()
        return obj