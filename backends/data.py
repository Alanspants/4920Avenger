# import requests
# import alpha_vantage
# from alpha_vantage.alphavantage import AlphaVantage
# ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co'
# QUERY_URL = ALPHA_VANTAGE_BASE_URL + '/query'
# params = {'function': 'FX_WEEKLY', 'from_currency': 'AUD', 'to_currency': 'USD', 'apikey': 'HCNWHBNAFIE8Q0EJ'}
#
# r = requests.get(QUERY_URL, params=params)
# print(r.json())

import requests
import alpha_vantage
from datetime import date
import datetime
from flask import jsonify

def getData(code):
    API_URL = "https://www.alphavantage.co/query"

    data = {
        "function": "FX_DAILY",
        "from_symbol": "AUD",
        "to_symbol": code,
        "apikey": "HCNWHBNAFIE8Q0EJ",
        }
    r = requests.get(API_URL, params=data).json()
    keys = []
    for i in range(1,30):
        n = -1 * i
        time = datetime.datetime.now() + datetime.timedelta(n)
        keys.append(str(time).split(" ")[0])

    values = []
    dates = []
    for i in range(29):
        if keys[i] not in r['Time Series FX (Daily)']:   
            continue
        values.append(r['Time Series FX (Daily)'][keys[i]]['1. open'])
        dates.append(keys[i])

    data = {}
    data["code"] = str(code)
    size = len(values)
    for i in range(size):
        data[str(i)] = {}
        data[str(i)]["date"] = str(dates[i])
        data[str(i)]["value"] = str(values[i])
    
    return jsonify(data)
    

    
        
                
        
