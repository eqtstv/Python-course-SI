import requests
import pandas as pd
import time

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
    

df = create_dataframe()
while True:
    update_prices(df, 5000)
    print(df.loc[:, ['Max Potential Profit [%]']].sort_values(by=['Max Potential Profit [%]'], ascending=False))
    print('')
    print('-'*30)
    time.sleep(300)
