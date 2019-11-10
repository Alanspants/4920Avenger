from backends.database import Database
from passlib.hash import pbkdf2_sha512

class User(object):
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def to_json(self):
        return {"name": self.name, "email": self.email, "password": self.password}

    def add_to_database(self):
        Database.add_new(document="users", new=self.to_json())

    @staticmethod
    def new_user(name, email, password):
        match = Database.match(document="users", new_record={"email": email})
        if match is not None:
            return False
        else:
            User(name, email, User.encode_password(password)).add_to_database()
            return True

    @staticmethod
    def get_user_by_email(email):
        return Database.match(document="users", new_record={"email": email})

    @staticmethod
    def encode_password(password):
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def validation_password(password, hash_password):
        return pbkdf2_sha512.verify(password, hash_password)

    @staticmethod
    def update_user_by_email(old, new):
        Database.update_record(document="users", new_record={"email":old}, new_query={"$set": {"email": new}})

    @staticmethod
    def validation(email, password):
        user = Database.match(document="users", new_record={"email": email})
        if user is None:
            return False
        if User.validation_password(password, user["password"]) is False:
            return False
        return True



