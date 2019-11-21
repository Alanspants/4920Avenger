def convert(fromCurrency, toCurrency, fromAmount, currencylist, pos):

    fC_sell = float(currencylist[pos[fromCurrency]].sell_rate)
    fC_buy = float(currencylist[pos[fromCurrency]].buy_rate)
    fC_average = (fC_sell + fC_buy) / 2

    tC_sell = float(currencylist[pos[toCurrency]].sell_rate)
    tC_buy = float(currencylist[pos[toCurrency]].buy_rate)
    tC_average = (tC_sell + tC_buy) / 2

    fC_amount = float(fromAmount)
    result = fC_average / tC_average
    result = fC_amount / result
    result = float(round(result, 2))
    return result
