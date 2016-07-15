
class Resources():
    GOLD = "GOLD"
    WOOD = "WOOD"
    STONE = "STONE"
    CRYSTALS = "CRYSTALS"
    
    def __init__(self):
        self.gold = 0
        self.wood = 0
        self.stone = 0
        self.crystals = 0
        
    def Add(self, resourceType, resourceAmount):
        if resourceType == Resources.GOLD:
            self.gold += resourceAmount
        elif resourceType == Resources.WOOD:
            self.wood += resourceAmount
        elif resourceType == Resources.STONE:
            self.stone += resourceAmount
        elif resourceType == Resources.CRYSTALS:
            self.crystals += resourceAmount