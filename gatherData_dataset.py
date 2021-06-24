import os
import mplfinance as mpf
import pandas as pd
import numpy as np
import datetime
import sys
import urllib.request
import json
import pandas_profiling
from binance.client import Client
from finta import TA
from scipy.signal import argrelextrema #for local highs/lows

#checking that we have 3 arguments (the validity of the arguments is tested later)
if(len(sys.argv)!=4):
    print("testAPI.py was called with the wrong amount of arguments")
    sys.exit()

#getting symbol and timeframe from command line
#this also checks whether the symbol exists on binance 
#retrieve LONG/SHORT ratio from binance's API
symbol = sys.argv[1]
timeframe = sys.argv[2]
amountDays = sys.argv[3]

try: 
    url = urllib.request.urlopen("https://fapi.binance.com/futures/data/topLongShortAccountRatio?symbol="+symbol+"&period=1h")
except urllib.error.HTTPError as exception:
    print('____________________________________________________')
    print("There was an error retrieving the long/short ratio from binance")
    print("Please check that your syntax was of the form 'BTCUSDT' or 'ETHUSDT'... for the symbol")
    print("And '5m' or '15m' or '1h'... for the timeframe")
    print('____________________________________________________')
    sys.exit()

## setting up binance API from environment variables ##
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')
client = Client(api_key, api_secret)

def valuesforDF():
    #fills dataframe with information : open, close, etc... & rsi, macd, bbands
    open,high,low,close,time,pandasdti,volume = [],[],[],[],[],[],[]
    for kline in client.get_historical_klines(symbol, timeframe, amountDays+"days ago UTC"):
        pandasdti.append(pd.to_datetime((datetime.datetime.fromtimestamp(kline[0]/1000).strftime('%Y-%m-%d %H:%M'))))
        open.append(float(kline[1]))
        high.append(float(kline[2]))
        low.append(float(kline[3]))
        close.append(float(kline[4]))
        volume.append(float(kline[5]))

    zippedList = list(zip(pandasdti, open, high, low, close))
    df = pd.DataFrame(zippedList, columns = ['datetime', 'open' , 'high', 'low', 'close'])
    df = df.set_index(['datetime'])
    df['volume'] = volume

    bband = TA.BBANDS(df)
    df['BB_MIDDLE'] = bband['BB_MIDDLE']
    df['BB_UPPER'] = bband['BB_UPPER']
    df['BB_LOWER'] = bband['BB_LOWER']
    bbwidth = TA.BBWIDTH(df)
    df['BBWIDTH'] = bbwidth
    macd = TA.MACD(df)
    df['MACD'] = macd['MACD']
    df['MACD_signal'] = macd['SIGNAL']
    RSI= TA.RSI(df)
    df['RSI'] = RSI
    BBp = TA.PERCENT_B(df)
    df["BBp"]= BBp
    ADX = TA.ADX(df)
    df['ADX'] = ADX
    DMI = TA.DMI(df)
    df['DMIp'] = DMI['DI+']
    df['DMIm'] = DMI['DI-']
    STOCH_K = TA.STOCH(df)
    STOCH_D = TA.STOCHD(df)
    df['STOCH_K'] = STOCH_K
    df['STOCH_D'] = STOCH_D
    OBV = TA.OBV(df)
    df['OBV'] = OBV


    # marking good places to buy and sell for dataset
    #__________________________________________________________#
    #plotting local lows for price
    df['buy'] = df.iloc[argrelextrema(df.close.values, np.less_equal,order=(10))[0]]['close']
    #plotting local highs for price
    df['sell'] = df.iloc[argrelextrema(df.close.values, np.greater_equal,order=(10))[0]]['close']
    #__________________________________________________________#
    
    df.loc[df.buy.notna(), 'buy_sell'] = 1
    df.loc[df.sell.notna(), 'buy_sell'] = -1
    df.loc[df.buy_sell.isnull(), 'buy_sell'] = 0 #needs changing

    df = df.drop(['buy', 'sell'], axis=1)
    df = df.dropna()

    #creating CSV file from the dataframe
    df.to_csv(r'dataset.txt', sep=',', mode='w+')
    #profileR = pandas_profiling.ProfileReport(df)
    #profileR.to_file("./report.html")
    print(df)


valuesforDF()

