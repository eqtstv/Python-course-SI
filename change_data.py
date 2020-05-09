import pandas as pd

def change_volume(file, crypto, volume):
    if crypto.upper() in ['BTC', 'ETH', 'LTC', 'XRP', 'BCH']:
        df = pd.read_csv(file)
        df.at[df['Currency'] == crypto.upper(), 'Volume'] = volume
        df.to_csv(file, index=False)
    else:
        print('We dont support this crypto')

def delete_crypto(file, crypto):
    df = pd.read_csv(file)
    if crypto.upper() in df['Currency'].values:
        df.drop(df.loc[df['Currency'] == crypto.upper()].index, inplace=True)
        df.to_csv(file, index=False)
    else:
        print('This crypto is not in wallet')

def add_crypto(file, crypto, volume):
    if crypto.upper() in ['BTC', 'ETH', 'LTC', 'XRP', 'BCH']:
        df = pd.read_csv(file)
        df = df.append({'Currency': crypto, 'Volume': volume}, ignore_index=True)
        df.to_csv(file, index=False)
    else:
        print('We dont support this crypto')

def main():
    print('What you want to do?')
    print('1: Change Volume')
    print('2: Add Currency')
    print('3: Delete Currency')
    print('0: Exit')
    choice = input()

    if choice == '1':
        print('Enter currenncy name:')
        cr = input()
        print('Enter new volume')
        vol = input()
        change_volume(wallet_file, cr, vol)
    if choice == '2':
        print('Enter currenncy name:')
        cr = input()
        print('Enter volume')
        vol = input()
        add_crypto(wallet_file, cr, vol)
    elif choice == '3':
        print('Enter currency to delete:')
        cr = input()
        delete_crypto(wallet_file, cr)
    elif choice == '0':
        return 0


print('Enter wallet filename:')
wallet_file = input() + '.csv'

while True:
    if main() == 0:
        break