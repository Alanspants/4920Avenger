from modles.database import Database
from passlib.hash import pbkdf2_sha512


class All_alert(object):
    def __init__(self, email, currency, rate_exchange, price):
        self.email = email
        self.currency = currency
        self.rate_exchange = rate_exchange
        self.price = price

    @staticmethod
    def create_alert(email, currency, rate_exchange, price):
        alert_data = Database.find_one(collection="all_alert", query={"email": email, "currency": currency, "rate_exchange": rate_exchange})
        if alert_data is not None:
            return False
        All_alert(email, currency, rate_exchange, price).save_to_db()
        return True

    def save_to_db(self):
        Database.insert(collection="all_alert", data=self.json())

    def json(self):
        return {
            "email": self.email,
            "currency": self.currency,
            "rate_exchange": self.rate_exchange,
            "price": self.price
        }

    @staticmethod
    def find_user_alert(email, rate_exchange):
        return Database.find(collection="all_alert", query={"email": email, "rate_exchange": rate_exchange})

    # @staticmethod
    # def update_user_email(old_email, email):
    #     Database.update(collection="users", query={"email": old_email}, data={"$set": {"email": email}})
