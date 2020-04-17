import requests
import pandas as pd
import time

def create_dataframe():
    df = pd.DataFrame(index=['bitbay', 'bitfinex', 'bitstamp', 'bittrex'])
    df['Buy Price'] = [0 for i in range(4)]
    df['Buy Amount'] = [0 for i in range(4)]
    df['Sell Price'] = [0 for i in range(4)]
    df['Sell Amount'] = [0 for i in range(4)]
    df['Taker'] = [1.025, 1.024, 1.025, 1.025]
    df['BTC'] = [0.3 for i in range(4)]
    df['USD'] = [2000 for i in range(4)]
    df['Profit'] = [0 for i in range(4)]
    return df

def update_exchanges(df):
    bitbay = requests.get('https://bitbay.net/API/Public/btcusd/orderbook.json').json()
    bitfinex = requests.get('https://api-pub.bitfinex.com/v2/book/tBTCUSD/P0').json()
    bitstamp = requests.get('https://www.bitstamp.net/api/order_book/').json()
    bittrex = requests.get('https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-BTC&type=both').json()

    df['Buy Price'] = [bitbay['asks'][0][0], bitfinex[25][0], float(bitstamp['asks'][0][0]), bittrex['result']['buy'][0]['Rate']]
    df['Buy Amount'] = [bitbay['asks'][0][1], abs(bitfinex[25][2]), float(bitstamp['asks'][0][1]), bittrex['result']['buy'][0]['Quantity']]
    df['Sell Price'] = [bitbay['bids'][0][0], bitfinex[0][0], float(bitstamp['bids'][0][0]), bittrex['result']['sell'][0]['Rate']]
    df['Sell Amount'] = [bitbay['bids'][0][1], bitfinex[0][2], float(bitstamp['bids'][0][1]), bittrex['result']['sell'][0]['Quantity']]

    return df

def arbitration(df):
    best_buy_idx = df['Buy Price'].idxmin()
    best_sell_idx = df['Sell Price'].idxmax()
    best_buy_price = df.loc[best_buy_idx, 'Buy Price']
    best_sell_price = df.loc[best_sell_idx, 'Sell Price']
    arbitration_amount = min(df.loc[best_buy_idx, 'Buy Amount'], df.loc[best_sell_idx, 'Sell Amount'], best_buy_price * df.loc[best_buy_idx, 'USD'], best_sell_price * df.loc[best_sell_idx, 'BTC'])
    profit_after_commision = best_sell_price * arbitration_amount *  1/df.loc[best_sell_idx, 'Taker']  - best_buy_price * arbitration_amount * df.loc[best_buy_idx, 'Taker']

    if df['Buy Price'].min() < df['Sell Price'].max():
        print('Na gieldzie {}, mozesz kupic {} BTC, po kursie ${} \ni sprzedac na gieldzie {} po kursie ${}, zyskujac ${}\n'.format(
            best_buy_idx, arbitration_amount, best_buy_price,
            best_sell_idx, best_sell_price,
            round((best_sell_price - best_buy_price) * arbitration_amount, 2)
        ))
        print('Po doliczeniu prowizji zysk bedzie wynosil: ${}'.format(
        round(profit_after_commision, 2)))

        if profit_after_commision > 0:
            df.loc[best_buy_idx, 'BTC'] += arbitration_amount
            df.loc[best_buy_idx, 'USD'] -= best_buy_price * arbitration_amount * df.loc[best_buy_idx, 'Taker']
            df.loc[best_sell_idx, 'BTC'] -= arbitration_amount
            df.loc[best_sell_idx, 'USD'] += best_sell_price * arbitration_amount *  1/df.loc[best_sell_idx, 'Taker']
            df.loc[best_sell_idx, 'Profit'] += round(profit_after_commision, 2)
            print('---> Arbitraz udany')
        else:
            print('---> Arbitraz niemozliwy przez prowizje\n')
    else:
        print('Arbitraz niemozliwy\n')


df = create_dataframe()

while True:
    print(update_exchanges(df))
    print('')
    arbitration(df)
    print('Total profit: ${}'.format(df['Profit'].sum()))
    print('-'*100)
    time.sleep(2)
