def convert(fromCurrency, toCurrency, fromAmount, currencylist, pos):
    # if(fromCurrency == -1):
    #     fC_average = 1
    # else:
    #     fC_sell = float(currencylist[pos[fromCurrency]].sell_rate)
    #     fC_buy = float(currencylist[pos[fromCurrency]].buy_rate)
    #     fC_average = (fC_sell + fC_buy) / 2
    # if(toCurrency == -1):
    #     tC_average = 1
    # else:
    #     tC_sell = float(currencylist[pos[toCurrency]].sell_rate)
    #     tC_buy = float(currencylist[pos[toCurrency]].buy_rate)
    #     tC_average = (tC_sell + tC_buy) / 2
    fC_sell = float(currencylist[pos[fromCurrency]].sell_rate)
    fC_buy = float(currencylist[pos[fromCurrency]].buy_rate)
    fC_average = (fC_sell + fC_buy) / 2

    tC_sell = float(currencylist[pos[toCurrency]].sell_rate)
    tC_buy = float(currencylist[pos[toCurrency]].buy_rate)
    tC_average = (tC_sell + tC_buy) / 2

    fC_amount = float(fromAmount)
    # print(fC_sell,fC_buy)
    # print(tC_buy,tC_sell)
    result = fC_average / tC_average
    result = fC_amount / result
    result = float(round(result, 2))
    return result
