import requests


def get_print_data():
    req = requests.get('https://bitbay.net/API/Public/btcusd/orderbook.json').json()
    print('Bids: {}\nAsks: {}\n'.format(req['bids'], req['asks']))

def compare_exchanges():
    bitbay = requests.get('https://bitbay.net/API/Public/btcusd/ticker.json').json()
    blockchain = requests.get('https://blockchain.info/ticker').json()

    print('Bitbay min ask $: {} \nBlockchain min ask $: {}'.format(bitbay['ask'], blockchain['USD']['buy']))
    print('Better to buy at: {}\n'.format('Bitbay' if bitbay['ask'] < blockchain['USD']['buy'] else 'Blockchain'))

    print('Bitbay max bid $: {} \nBlockchain max bid $: {}'.format(bitbay['bid'], blockchain['USD']['sell']))
    print('Better to sell at: {}'.format('Bitbay' if bitbay['bid'] > blockchain['USD']['sell'] else 'Blockchain'))
    
get_print_data()
compare_exchanges()
