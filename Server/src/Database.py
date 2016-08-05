from Buildings import * # must be
from Data import dbLock
import Data
import pickle
import Config
import Log

class Database():
    lastSave = 0
    run = True
    
    @staticmethod
    def InitDatabase():
        Log.Save("Init database.\n")
        Data.mainData.Init()
        Database.lastSave = time.localtime(time.time())
        
    @staticmethod
    def LoadDatabase(): 
        Log.Save("Load database.\n") 
        Data.mainData.Load(Database.Load()) 
        Database.lastSave = time.localtime(time.time())
    
    @staticmethod
    def DatabaseSaver():
        try:
            while Database.run:
                actualTime = time.localtime(time.time())
                if Database.lastSave.tm_year < actualTime.tm_year or \
                   Database.lastSave.tm_mon < actualTime.tm_mon or \
                   Database.lastSave.tm_mday < actualTime.tm_mday or \
                   Database.lastSave.tm_hour < actualTime.tm_hour or \
                   Database.lastSave.tm_min < actualTime.tm_min or \
                   Database.lastSave.tm_sec + 2 < actualTime.tm_sec:
                    with dbLock:
                        Database.Save(Data.mainData)
                    Database.lastSave = actualTime
                    Log.Save("Database saved.\n")
        except Exception as inst:
            Log.Save(inst.__str__() + "\n")
            Log.Save("Database saving crashed.\n")
        Log.Save("Stop saving database.\n")
                
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