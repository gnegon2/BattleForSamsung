import Units
import Statistics
from Player import Player

player1 = Player("Asd")
player2 = Player("A")
player1.username = "ASD"
player2.username = "A"
player1.InitUserInfo()
player2.InitUserInfo()

u1 = Units.Peasant(player1)
u2 = Units.Peasant(player2)
u3 = Units.Cannon(player2)

print id(u1.statistics)
print id(u2.statistics)
print id(u3.statistics)

