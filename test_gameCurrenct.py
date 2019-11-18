from backends.database import Database
from backends.gamer import Gamer

Database.setup()
gamer1 = Gamer.new_gamer("gamer1", "gamer1@test.com")
gamer1.update_gameCurrency("AUD","200","CNY")
print(gamer1.get_message())
print(Database.get_all(document="game").count())
print(Database.get_all(document="game")[0])
print(Database.get_all(document="game")[0]["amount"])



# for gamer in Database.get_all(document="game"):
#     print(gamer.get_email())