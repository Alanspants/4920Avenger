from backends.database import Database
from passlib.hash import pbkdf2_sha512

class Reminder(object):
    def __init__(self, email, currency, price):
        self.email = email
        self.currency = currency
        self.price = price


    def to_json(self):
        return {
            "email": self.email, "currency": self.currency, "price": self.price}

    def add_to_database(self):
        Database.add_new(document="all_alert", new=self.to_json())

    @staticmethod
    def new_reminder(email, currency, price):
        match = Database.match(document="all_alert", new_record={"email": email, "currency": currency})
        if match is not None:
            return False
        else:
            Reminder(email, currency, price).add_to_database()
            return True

    @staticmethod
    def get_reminder_by_email(email):
        return Database.find(document="all_alert", new_record={"email": email})

    @staticmethod
    def update_reminder(email, currency, price):
        Database.update_record(document="all_alert", new_record={"email":email, "currency": currency}, new_query={"$set": {"price": price}})

    @staticmethod
    def delete_reminder(email, currency):
        Database.delete_record(document="all_alert", old={"email": email, "currency": currency})
