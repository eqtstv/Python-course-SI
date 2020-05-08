import requests
import pandas as pd

def get_price(crypto, currency = 'usd'):
    return float(requests.get('https://www.bitstamp.net/api/v2/ticker/{}{}/'.format(crypto.lower(), currency.lower())).json()['bid'])

def get_price_t_24(crypto, currency = 'usd'):
    return float(requests.get('https://www.bitstamp.net/api/v2/transactions/{}{}/'.format(crypto.lower(), currency.lower()), params={'time': 'day'}).json()[-1]['price'])

def change_volume(crypto, volume):
    if crypto.upper() in ['BTC', 'ETH', 'LTC', 'XRP', 'BCH']:
        df = pd.read_csv('my_currencies.csv')
        df.at[df['Currency'] == crypto.upper(), 'Volume'] = volume
        df.to_csv('my_currencies.csv', index=False)
    else:
        print('We dont support this crypto')

def update_data(currency = 'usd'):
    df =  pd.read_csv('my_currencies.csv')
    df['Current Price'] = df['Currency'].apply(get_price, currency)
    df['Price t-24'] = df['Currency'].apply(get_price_t_24, currency)
    df['Current Value'] = df['Current Price'] * df['Volume']
    df['Value t-24'] = df['Price t-24'] * df['Volume']
    df['Profit [{}]'.format('$' if currency == 'usd' else '€')] = df['Current Value'] - df['Value t-24']
    df['Profit [%]'] = round((df['Current Price'] - df['Price t-24'])*100 / df['Current Price'], 2)
    df.sort_values(['Profit [%]'], ascending=False, inplace=True)
    return df

df = update_data()
print(df)