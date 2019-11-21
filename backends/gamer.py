from backends.currency import Source
from backends.database import Database
from backends.calculator import convert


class Gamer(object):

    def __init__(self, name, email):
        self.currencylist, self.pos = Source.get_currency()
        self.name = name
        self.email = email
        self.gameCurrency = {}
        for index in self.pos:
            self.gameCurrency[index] = 0
        self.gameCurrency["AUD"] = 1000
        self.amount = 1000

    def get_email(self):
        return self.email

    def to_json(self):
        return {"name": self.name, "email": self.email, "gameCurrency": self.gameCurrency, "amount": self.amount}

    def add_to_database(self):
        Database.add_new(document="game", new=self.to_json())

    # def update_gameCurrency(self, from_currency, from_amount, to_currency):
    #     to_amount = convert(from_currency, to_currency, from_amount, self.currencylist, self.pos)
    #     # self.gameCurrency[from_currency] -= from_amount
    #     # self.gameCurrency[to_currency] = to_amount
    #     temp_gameCurrency = self.gameCurrency
    #     temp_gameCurrency[from_currency] = float(temp_gameCurrency[from_currency]) - float(from_amount)
    #     temp_gameCurrency[to_currency] = to_amount
    #     print(temp_gameCurrency)
    #     #     currencylist, pos = Source.get_currency()
    #     Database.update_record(document="game", new_record={"name":self.name}, new_query={"$set": {"gameCurrency": temp_gameCurrency }})
    #     self.gameCurrency = temp_gameCurrency
    #     self.update_amount()
    #
    # def update_amount(self):
    #     ans = 0
    #     for currency in self.gameCurrency:
    #         temp = convert(currency, "AUD", self.gameCurrency[currency], self.currencylist, self.pos)
    #         ans += temp
    #     print("New Amount: ", ans)
    #     Database.update_record(document="game", new_record={"amount": self.amount},
    #                            new_query={"$set": {"game": ans}})
    #     self.amount = ans

    # def get_message(self):
    #     ans = ""
    #     for currency in self.gameCurrency:
    #         if(self.gameCurrency[currency] != 0):
    #             ans = ans + str(currency) + ": " + str(self.gameCurrency[currency]) + "\n"
    #     return ans

    @staticmethod
    def new_gamer(name, email):
        Gamer(name, email).add_to_database()
        return Gamer(name, email)

    @staticmethod
    def get_gamer_by_name(name):
        gamer = Database.match(document="game", new_record={"name": name})
        return gamer

    @staticmethod
    def update_amount(name):
        currencylist, pos = Source.get_currency()
        gamer = Gamer.get_gamer_by_name(name)
        ans = 0
        for currency in gamer["gameCurrency"]:
            temp = convert(currency, "AUD", gamer["gameCurrency"][currency], currencylist, pos)
            ans += temp
        Database.update_record(document="game", new_record={"name": name},
                               new_query={"$set": {"amount": ans}})
        return ans

    @staticmethod
    def get_amount(name):
        currencylist, pos = Source.get_currency()
        gamer = Gamer.get_gamer_by_name(name)
        ans = 0
        for currency in gamer["gameCurrency"]:
            temp = convert(currency, "AUD", gamer["gameCurrency"][currency], currencylist, pos)
            ans += temp

        return ans


    @staticmethod
    def update_gameCurrency(name, from_currency, to_currency, from_amount):
        currencylist, pos = Source.get_currency()
        to_amount = convert(from_currency, to_currency, from_amount, currencylist, pos)
        temp_gameCurrency = Gamer.get_gamer_by_name(name)["gameCurrency"]
        temp_gameCurrency[from_currency] = float(temp_gameCurrency[from_currency]) - float(from_amount)
        temp_gameCurrency[to_currency] = float(temp_gameCurrency[to_currency]) + float(to_amount)
        Database.update_record(document="game", new_record={"name": name},
                               new_query={"$set": {"gameCurrency": temp_gameCurrency}})
        print(Gamer.get_gamer_by_name(name)["gameCurrency"])
        Gamer.update_amount(name)

    @staticmethod
    def get_available_currency(name):
        gamer = Gamer.get_gamer_by_name(name)
        # ans = {}
        # for currency in gamer["gameCurrency"]:
        #     if gamer["gameCurrency"][currency] != 0:
        #         ans[currency] = gamer["gameCurrency"][currency]
        ans = []
        for currency in gamer["gameCurrency"]:
            if gamer["gameCurrency"][currency] != 0:
                ans.append(currency)
        return ans

    @staticmethod
    def get_message(name):
        gamer = Gamer.get_gamer_by_name(name)
        ans = ""
        for currency in gamer["gameCurrency"]:
            if gamer["gameCurrency"][currency] != 0:
                ans += str(currency) + "   :   " + str(gamer["gameCurrency"][currency]) + "\n"
        return ans




    # def all_gameCurrency(self):
    #     currencylist, pos = Source.get_currency()
    #     for index in pos:
    #         print(index, self.gameCurrency[index])
