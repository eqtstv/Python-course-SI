import requests
import pandas as pd
import time

def create_dataframe():
    df = pd.DataFrame(index=['BTC', 'ETH', 'Dash', 'LTC', 'LSK'])
    df['Current Buy'] = [0 for i in range(5)]
    df['Current Sell'] = [0 for i in range(5)]
    df['Min Buy'] = [float("inf") for i in range(5)]
    df['Max Sell'] = [0 for i in range(5)]
    df['Max Potential Profit [%]'] = [0 for i in range(5)]
    return df

def update_prices(df, investment = float("inf")):
    btc = requests.get('https://bitbay.net/API/Public/btcusd/orderbook.json').json()
    eth = requests.get('https://bitbay.net/API/Public/ethusd/orderbook.json').json()
    dash = requests.get('https://bitbay.net/API/Public/dashusd/orderbook.json').json()
    ltc = requests.get('https://bitbay.net/API/Public/ltcusd/orderbook.json').json()
    lsk = requests.get('https://bitbay.net/API/Public/lskusd/orderbook.json').json()

    best_sell = []
    best_buy = []
    
    for currency in [btc, eth, dash, ltc, lsk]:
        best_sell.append((next(bid[0] for bid in currency['bids'] if bid[1] < investment / bid[0])))
        best_buy.append((next(bid[0] for bid in currency['asks'] if bid[1] < investment / bid[0])))

    df['Current Sell'] = best_sell
    df['Current Buy'] = best_buy
    df['Min Buy'] = df[['Current Buy', 'Min Buy']].min(axis=1)
    df['Max Sell'] = df[['Current Sell', 'Max Sell']].max(axis=1)
    df['Max Potential Profit [%]'] = round((df['Max Sell'] - df['Min Buy'])*100 / df['Min Buy'], 6)
    

df = create_dataframe()
while True:
    update_prices(df)
    #print(df.sort_values(by=['Max Potential Profit [%]'], ascending=False))
    print(df.loc[:, ['Max Potential Profit [%]']].sort_values(by=['Max Potential Profit [%]'], ascending=False))
    print('')
    print('-'*30)
    time.sleep(2)