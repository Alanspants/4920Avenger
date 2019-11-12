from backends.database import Database

Database.setup()


print(Database.match(document="test", new_record={"name":"dolly"}))
print(Database.find(document="test",new_record={"age":"3"}))
print(Database.get_all(document="test"))
print(Database.get_all(document="test")[0])
print(Database.get_all(document="test")[1])
