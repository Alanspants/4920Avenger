import pandas as pd
import ssl

class Money(object):
    def __init__(self, currency, code, sell_rate, buy_rate):
        self.currency = currency
        self.code = code
        self.sell_rate = sell_rate
        self.buy_rate = buy_rate

    @staticmethod
    def search_data():
        ssl._create_default_https_context = ssl._create_unverified_context
        data = pd.read_html("https://www.wexchange.com.au/exchange-rates/")[0]
        pd.set_option('display.width',None)
        data.columns = ["Currency", "Code", "Sell Rate", "Delete", "Buy Rate"]
        data["Currency"] = data["Currency"].str.replace(r'\((.)+$', '').str.strip()
        data.drop(["Delete"], inplace=True, axis=1)
        currency_name = data['Currency']
        moneydict = {}
        position = {}
        for i in range(0, 42):
            dollar = data.values[i]
            moneydict[i] = Money(dollar[0], dollar[1], dollar[2], dollar[3])
            position[currency_name[i][0]] = i
        return moneydict, position
#http://www.ezybonds.com/exchange.asp

'''
test
moneydict, position = Money.search_data()

for i in range(0, 42):
    print(moneydict[i].currency)
    print(moneydict[i].code)
    print(moneydict[i].sell_rate)
    print(moneydict[i].buy_rate)
'''