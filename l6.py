import requests
import pandas as pd
import time
import json

def create_dataframe():
    df = pd.DataFrame(index=['BTC', 'ETH', 'Dash', 'LTC', 'LSK'])
    df['Current Price'] = [0 for i in range(5)]
    df['Min Price'] = [float("inf") for i in range(5)]
    df['Max Price'] = [0 for i in range(5)]
    df['Max Potential Profit [%]'] = [0 for i in range(5)]
    return df

def update_prices(df, investment = float("inf")):
    btc = requests.get('https://bitbay.net/API/Public/btcusd/orderbook.json').json()['bids']
    eth = requests.get('https://bitbay.net/API/Public/ethusd/orderbook.json').json()['bids']
    dash = requests.get('https://bitbay.net/API/Public/dashusd/orderbook.json').json()['bids']
    ltc = requests.get('https://bitbay.net/API/Public/ltcusd/orderbook.json').json()['bids']
    lsk = requests.get('https://bitbay.net/API/Public/lskusd/orderbook.json').json()['bids']

    best_prices_vol = []
    for curr in [btc, eth, dash, ltc, lsk]:
        best_prices_vol.append((next(bid[0] for bid in curr if bid[1] < investment / bid[0])))

    df['Current Price'] = best_prices_vol
    df['Min Price'] = df[['Current Price', 'Min Price']].min(axis=1)
    df['Max Price'] = df[['Current Price', 'Max Price']].max(axis=1)
    df['Max Potential Profit [%]'] = round((df['Max Price'] - df['Min Price'])*100 / df['Min Price'], 6)

def get_price(currency, volume):
    return float(requests.get('https://www.bitstamp.net/api/v2/ticker/{}usd/'.format(currency)).json()['bid']) * volume

def get_price_t_24(currency, volume):
    return float(requests.get('https://www.bitstamp.net/api/v2/transactions/{}usd/'.format(currency), params={'time': 'day'}).json()[-2500]['price']) * volume

#min(data, key=lambda x:abs(x-1588857180))
btc = get_price('btc', 1)
btc_24 = get_price_t_24('btc', 1)

print(round((btc - btc_24)*100 / btc, 2))
print((btc / btc_24 - 1)*100)

#df = create_dataframe()
#df.index.name = 'Currency'
#update_prices(df, 5000)
#df.sort_values(by=['Max Potential Profit [%]'], ascending=False, inplace=True)
#df.to_csv('database.csv')

#my_curr = pd.read_csv('my_currencies.csv')
#print(my_curr.sort_values(['Volume'], ascending=False))

