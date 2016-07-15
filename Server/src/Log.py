import Config

class Log():
    @staticmethod
    def Init():
        text = "Init log.\n"
        
        logFile = open(Config.logPath, 'w')
        logFile.write(text)
        logFile.close()
        
        if Config.debug:
            print text
            
    @staticmethod
    def Save(text):
        logFile = open(Config.logPath, 'a')
        logFile.write(text)
        logFile.close()
        
        if Config.debug:
            print text
            