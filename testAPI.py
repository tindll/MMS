import os
import mplfinance as mpf
import pandas as pd
import numpy as np
import datetime
from binance.client import Client

## setting up binance API from environment variables ##
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')
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

#candles = client.get_klines(symbol='BNBBTC', interval=Client.KLINE_INTERVAL_30MINUTE)
#print(candles)
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "7 day ago UTC")
print(klines)
#tickers = client.get_orderbook_tickers()
for kline in client.get_historical_klines_generator("BNBBTC", Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC"):
    print(kline)
    # do something with the kline
