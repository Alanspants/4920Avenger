from modles.database import Database

Database.initialize()
Database.insert(collection="test",data={"name":"alan","age":"18"})
Database.insert(collection="test",data={"name":"dolly","age":"18"})
print(Database.find_one(collection="test",query={"name":"alan"}))
print(Database.find(collection="test",query={"age":"18"})[0])
print(Database.find(collection="test",query={"age":"18"})[1])
print(Database.find_all(collection="test")[0])
print(Database.find_all(collection="test")[1])