import requests
import pandas as pd

def get_price(crypto, currency = 'usd'):
    return float(requests.get('https://www.bitstamp.net/api/v2/ticker/{}{}/'.format(crypto.lower(), currency.lower())).json()['bid'])

def get_price_t_24(crypto, currency = 'usd'):
    return float(requests.get('https://www.bitstamp.net/api/v2/transactions/{}{}/'.format(crypto.lower(), currency.lower()), params={'time': 'day'}).json()[-1]['price'])

def update_data(file, currency = 'usd'):
    df =  pd.read_csv(file)
    df['Current Price'] = round(df['Currency'].apply(get_price, currency), 2)
    df['Price t-24'] = round(df['Currency'].apply(get_price_t_24, currency), 2)
    df['Current Value'] = round(df['Current Price'] * df['Volume'], 2)
    df['Value t-24'] = round(df['Price t-24'] * df['Volume'], 2)
    df['Profit [{}]'.format('$' if currency == 'usd' else '€')] = round(df['Current Value'] - df['Value t-24'], 2)
    df['Profit [%]'] = round((df['Current Price'] - df['Price t-24'])*100 / df['Price t-24'], 2)
    df.sort_values(['Profit [%]'], ascending=False, inplace=True)
    return df, currency

def wallet_chagnge_currency(df):
    return round(df['Current Value'].sum() - df['Value t-24'].sum(), 2)

def wallet_chagnge_percent(df):
    return round((df['Current Value'].sum() - df['Value t-24'].sum()) * 100 / df['Value t-24'].sum(), 2)

def run_wallet(file):
    df, currency = update_data(file)
    print(df)
    print('\nWallet change in 24h: {}{}\nWallet change in 24h: {}%'.format('$' if currency == 'usd' else '€', wallet_chagnge_currency(df), wallet_chagnge_percent(df)))


print('Enter wallet filename:')
wallet_file = input() + '.csv'
run_wallet(wallet_file)