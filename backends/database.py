import pymongo

class Database(object):
    mongo_port = 27017
    mongo_host = 'localhost'
    db_name = None
    @staticmethod
    def setup():
        client = pymongo.MongoClient(host=Database.mongo_host, port=Database.mongo_port)
        Database.db_name = client['currency']

    @staticmethod
    def add_new(document, new):
        Database.db_name[document].insert(new)

    @staticmethod
    def get_all(document):
        return Database.db_name[document].find()

    # find one record
    @staticmethod
    def match(document, new_record):
        return Database.db_name[document].find_one(new_record)

    # find
    @staticmethod
    def find(document, new_record):
        return Database.db_name[document].find(new_record)

    @staticmethod
    def update_record(document, new_record, new_query):
        Database.db_name[document].update(new_record, new_query)


    @staticmethod
    def delete_record(document, old):
        Database.db_name[document].remove(old)
