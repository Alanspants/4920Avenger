import pymongo

# clien = pymongo.MongoClient(['mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb'])
# client = pymongo.MongoClient(['localhost:27017'])
# DATABASE = client['class']
# DATABASE['student'].insert_one({"name":"oj","age":"14"})
# DATABASE['student'].insert_one({"name":"alan","age":"18"})
# # print(DATABASE['student'].find_one({"name":"alan","age":"18"}))
# DATABASE['student'].remove({"name":"oj"})

class Database(object):
    URL = ['localhost:27017']
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URL)
        Database.DATABASE = client['currency']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_all(collection):
        return Database.DATABASE[collection].find()

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)