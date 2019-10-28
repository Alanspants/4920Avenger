from modules.database import Database

Database.initialize()


print(Database.find_one(collection="test", query={"name":"dolly"}))
print(Database.find(collection="test",query={"age":"3"}))
print(Database.find_all(collection="test"))
print(Database.find_all(collection="test")[0])
print(Database.find_all(collection="test")[1])
