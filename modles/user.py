from modles.database import Database
from passlib.hash import pbkdf2_sha512

class User(object):
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def save_to_db(self):
        Database.insert(collection="user",data=self.json())

    def json(self):
        return {
            "name":self.name,
            "email":self.email,
            "password":self.password
        }

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hash_password(password, hash_password):
        return pbkdf2_sha512.verify(password,hash_password)