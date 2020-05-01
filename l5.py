import requests
import pandas as pd
import time

def create_dataframe():
    df = pd.DataFrame(index=['BTC', 'ETH', 'Dash', 'LTC', 'LSK'])
    df['Start Price'] = [0 for i in range(5)]
    df['Current Price'] = [0 for i in range(5)]
    df['Min Price'] = [9999999999 for i in range(5)]
    df['Max Price'] = [0 for i in range(5)]
    df['Profit [%]'] = [0 for i in range(5)]
    return df

def update_prices():
    btc = requests.get('https://bitbay.net/API/Public/btcusd/ticker.json').json()['bid']
    eth = requests.get('https://bitbay.net/API/Public/ethusd/ticker.json').json()['bid']
    dash = requests.get('https://bitbay.net/API/Public/dashusd/ticker.json').json()['bid']
    ltc = requests.get('https://bitbay.net/API/Public/ltcusd/ticker.json').json()['bid']
    lsk = requests.get('https://bitbay.net/API/Public/lskusd/ticker.json').json()['bid']

    return [btc, eth, dash, ltc, lsk]
    
def update_df(df):
    df['Current Price'] = update_prices()
    df['Min Price'] = df[['Current Price', 'Min Price']].min(axis=1)
    df['Max Price'] = df[['Current Price', 'Max Price']].max(axis=1)
    df['Profit [%]'] = round((df['Max Price'] - df['Min Price'])*100 / df['Start Price'], 6)
    return df

df = create_dataframe()
df['Start Price'] = update_prices()

while True:
    update_df(df)
    print(df.sort_values(by=['Profit [%]'], ascending=False))
    #print(df.loc[:, ['Profit [%]']].sort_values(by=['Profit [%]'], ascending=False))
    print('')
    print('-'*20)
    time.sleep(2)