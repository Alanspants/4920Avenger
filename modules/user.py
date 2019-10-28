from modules.database import Database
class User(object):
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def save_to_db(self):
         Database.insert(collection="users",data=self.json())

    def json(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }