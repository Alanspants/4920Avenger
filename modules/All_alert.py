from modules.database import Database
from passlib.hash import pbkdf2_sha512

class All_alert(object):
    def __init__(self, email, currency, price):
        self.email = email
        self.currency = currency
        self.price = price

    @staticmethod
    def create_alert(email, currency, price):
        alert_data = Database.find_one(collection="all_alert",
                                       query={"email": email, "currency": currency})
        if alert_data is not None:
            return False
        All_alert(email, currency, price).save_to_db()
        return True


    def save_to_db(self):
        Database.insert(collection="all_alert", data=self.json())

    def json(self):
        return {
            "email": self.email,
            "currency": self.currency,
            "price": self.price
        }


    @staticmethod
    def find_user_alert(email):
        return Database.find(collection="all_alert", query={"email": email})

    @staticmethod
    def delete_user_alert(email, currency):
        Database.delete(collection="all_alert",
                             query={"email": email, "currency": currency})

    @staticmethod
    def update_user_alert(email, currency, price):
        Database.update(collection="all_alert", query={"email":email, "currency": currency}, data={"$set": {"price": price}})