import requests
import pandas as pd
import time

def create_dataframe():
    df = pd.DataFrame(index=['bitbay', 'blockchain', 'bitstamp', 'coinbase'])
    df['Buy Price'] = [0 for i in range(4)]
    df['Sell Price'] = [0 for i in range(4)]
    df['Taker'] = [1.025, 1.024, 1.025, 1.05]
    df['BTC'] = [0.3 for i in range(4)]
    df['USD'] = [2000 for i in range(4)]
    df['Profit'] = [0 for i in range(4)]
    return df


def update_exchanges(df):
    bitbay = requests.get('https://bitbay.net/API/Public/btcusd/ticker.json').json()
    blockchain = requests.get('https://blockchain.info/ticker').json()
    bitstamp = requests.get('https://www.bitstamp.net/api/v2/ticker_hour/btcusd/').json()
    coinbase_buy = float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/buy.json').json()['data']['amount'])
    coinbase_sell = float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/sell.json').json()['data']['amount'])

    df['Buy Price'] = [bitbay['ask'], blockchain['USD']['buy'], float(bitstamp['ask']), coinbase_buy]
    df['Sell Price'] = [bitbay['bid'],  blockchain['USD']['sell'], float(bitstamp['bid']), coinbase_sell]

    return df

def arbitration(df):
    print('Best buy: {} {}'.format(df['Buy Price'].idxmin(), df['Buy Price'].min()))
    print('Best sell: {} {}'.format(df['Sell Price'].idxmax(), df['Sell Price'].max()))

    if df['Buy Price'].min() < df['Sell Price'].max():
        return True
    else:
        return False


df = create_dataframe()

while True:
    print(update_exchanges(df))
    print('')
    print('Arbitration viable: {}'.format(arbitration(df)))
    print(df['Profit'].sum())
    print('-'*60)
    time.sleep(5)