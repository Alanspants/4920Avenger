from backends.database import Database
from backends.gamer import Gamer

#1. 对所有gamer对amount进行loop
    # 先count 再loop
def rank():
    Database.setup()
    gamer_count = Database.get_all(document="game").count()
    sort_amount = {}
    for index in range(0,gamer_count):
        sort_amount[Database.get_all(document="game")[index]["name"]] = Database.get_all(document="game")[index]["amount"]
    # print(sort)
    sorted_amount = sorted(sort_amount.items(), key=lambda kv: kv[1], reverse=True)
    print(sort_amount)
    print(sorted_amount)
    return sorted_amount

# ans = rank()
# print(ans[0][0])
