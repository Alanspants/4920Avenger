import pandas

class Money(object):
    def __init__(self, currency, cash_in, cash_out, sign_in, sign_out):
        self.currency = currency
        self.cash_in = cash_in
        self.cash_out = cash_out
        self.sign_in = sign_in
        self.sign_out = sign_out

    @staticmethod
    def search_data():
        data = pandas.read_html("https://rate.bot.com.tw/xrt?Lang=zh-TW")[0]
        currency_table = data.ix[:,0:5]
        currency_table.columns = ["Currency","Cash_in","Cash_out","Sign_in", "Sign_out",]
        currency_table["Currency"] = currency_table["Currency"].str.extract("\((\w+)\)",expand=True)
        #print(currency_table)

        moneydict = {}
        position = {}
        for index in range(0, 19):
            dollar = currency_table.values[index]
            moneydict[index] = Money(dollar[0], dollar[1], dollar[2], dollar[3], dollar[4])
            position[dollar[0]] = index
        return moneydict, position

# moneydict, position = Money.search_data()
# print(position)
