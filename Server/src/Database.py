import pickle
import Config

class Database():
    @staticmethod
    def Save(obj):
        outputFile = open(Config.dataPath, 'wb')
        pickle.dump(obj, outputFile, -1)
        outputFile.close()
    @staticmethod
    def Load(): 
        inputFile = open(Config.dataPath, 'rb')
        obj = pickle.load(inputFile)
        inputFile.close()
        return obj