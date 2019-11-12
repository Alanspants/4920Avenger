from backends.database import Database

class WatchList(object):
    def __init__(self, email, currency, code, sell_rate, buy_rate):
        self.email = email
        self.currency = currency
        self.code = code
        self.sell_rate = sell_rate
        self.buy_rate = buy_rate

    def to_json(self):
        return {
            "email": self.email, "currency": self.currency, "code": self.code, "sell_rate": self.sell_rate, "buy_rate": self.buy_rate}

    def add_to_database(self):
        Database.add_new(document="preference", new=self.to_json())

    @staticmethod
    def new_watchList(email, currency, code, sell_rate, buy_rate):
        match = Database.match(document="preference", new_record={"email": email, "code": code})
        if match is not None:
            return False
        else:
            WatchList(email, currency, code, sell_rate, buy_rate).add_to_database()
            return True

    @staticmethod
    def get_watch_list(email):
        return Database.find(document="preference", new_record={"email": email})

    @staticmethod
    def delete_watchList(email, code):
        Database.delete_record(document="preference", old={"email": email, "code": code})