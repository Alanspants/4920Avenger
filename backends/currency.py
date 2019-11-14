import pandas as pd
import ssl

class Source(object):
    def __init__(self, currency, code, sell_rate, buy_rate):
        self.currency = currency
        self.code = code
        self.sell_rate = sell_rate
        self.buy_rate = buy_rate

    @staticmethod
    def get_currency():
        ssl._create_default_https_context = ssl._create_unverified_context
        data = pd.read_html("https://www.wexchange.com.au/exchange-rates/")[0]
        pd.set_option('display.width',None)
        data.columns = ["Currency", "Code", "Sell Rate", "Delete", "Buy Rate"]
        data["Currency"] = data["Currency"].str.replace(r'\((.)+$', '').str.strip()
        data.drop(["Delete"], inplace=True, axis=1)
        currencypos = {}
        currencylist = {}
        currency_name = data['Code']
        for pos in range(0, 42):
            currencypos[currency_name.values[pos]] = pos
            elements = data.values[pos]
            currencylist[pos] = Source(elements[0], elements[1], elements[2], elements[3])
        currencypos["AUD"] = 43
        currencylist[43] = Source("AUSTRALIAN DOLLAR","AUD","1","1")
        return currencylist, currencypos
#http://www.ezybonds.com/exchange.asp

#test
# currencylist, currencypos = Source.get_currency()
# print(currencylist[currencypos['AED']].sell_rate)



'''
# test
# list, cp = Money.search_data()
# 
# for i in range(0, 42):
#     print(list[i].currency)
#     print(list[i].code)
#     print(list[i].sell_rate)
#     print(list[i].buy_rate)
'''