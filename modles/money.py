import pandas

data = pandas.read_html("https://rate.bot.com.tw/xrt?Lang=zh-TW")[0]
currency_table = data.ix[:,0:5]
currency_table.columns = ["Currency","Currency-Buy","Currency-Sell","RealTime-Buy", "RealTime-Sell",]
currency_table["Currency"] = currency_table["Currency"].str.extract("\((\w+)\)",expand=True)
print(currency_table)