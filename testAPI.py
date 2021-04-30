import os

from binance.client import Client

# init
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')

#api key and secret to local variable
client = Client(api_key, api_secret)
#client.API_URL = 'https://testnet.binance.vision/api'


# get balances for all assets & some account information
#print(client.get_account())


# get balance for a specific asset only (BTC)
#print(client.get_asset_balance(asset='BTC'))


# get balances for futures account
print(client.futures_account_balance())


# get balances for margin account
#print(client.get_margin_account())


# get latest price from Binance API
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
# print full output (dictionary)
print(btc_price)

#example for btc_price[symbol or price]
#{'symbol': 'BTCUSDT', 'price': '9678.08000000'}
#We can access just the price as follows.
#print(btc_price["price"])
