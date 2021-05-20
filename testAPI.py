import os
import mplfinance as mpf
import pandas as pd
import numpy as np
import datetime
from binance.client import Client
from finta import TA
from scipy.signal import argrelextrema #for local highs/lows

## setting up binance API from environment variables ##
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')
client = Client(api_key, api_secret)

# get balances for all assets & some account information
#print(client.get_account())
# get balance for a specific asset only (BTC)
#print(client.get_asset_balance(asset='BTC'))

# get balances for futures account
print(client.futures_account_balance())

# get latest price from Binance API
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
# print full output (dictionary)
print(btc_price)
#example for btc_price[symbol or price]
#{'symbol': 'BTCUSDT', 'price': '9678.08000000'}
#We can access just the price as follows.
#print(btc_price["price"])
def create_plot(df):
    mc = mpf.make_marketcolors(up='w',down='b')
    s  = mpf.make_mpf_style(marketcolors=mc)
    ap0 = [ mpf.make_addplot(df['BB_UPPER'],color='cyan'), #BBANDS
            mpf.make_addplot(df['BB_LOWER'],color='cyan'), #BBANDS
            mpf.make_addplot(df['BB_MIDDLE'],color='grey'), #BBANDS
            mpf.make_addplot(df["RSI"], panel='lower', color='purple', ylabel="RSI"),
            mpf.make_addplot(df["MACD"], panel=3, color='red', ylabel="MACD"),
            mpf.make_addplot(df["MACD_signal"], panel=3, color='orange'),
            mpf.make_addplot(df["min"],type='scatter',markersize=25,color='red',marker='^'),
            mpf.make_addplot(df["max"],type='scatter',markersize=25,color='green',marker='v'),
            #mpf.make_addplot(df["RSImin"],type='scatter',panel='lower',markersize=25,color='red',marker='^'),
            #mpf.make_addplot(df["RSImax"],type='scatter',panel='lower',markersize=25,color='green',marker='v')
          ]





    mpf.plot(df, type='candle', axtitle = "BTCUSDT 1H (7D)", xrotation=20, datetime_format=' %A, %d-%m-%Y', savefig='chart.png', volume = True, volume_panel=2, style = s,addplot=ap0, fill_between=dict(y1=df['BB_LOWER'].values, y2=df['BB_UPPER'].values, alpha=0.15))
    vls=['2021-05-13 23:00','2021-05-20 12:00']
    mpf.plot(df,vlines=dict(vlines=vls,colors=('r','g')))
    mpf.plot(df,vlines=dict(vlines=vls,colors='c'))

def valuesforDF():
    #fills dataframe with information : open, close, etc... & rsi, macd, bbands
    open,high,low,close,time,pandasdti,volume = [],[],[],[],[],[],[]
    for kline in client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "7 day ago UTC"):
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


    #dataframe information for divergences (find_divergences())
    #__________________________________________________________#
    #order in iloc filters for noise
    #price
    #plotting local lows for price
    df['min'] = df.iloc[argrelextrema(df.close.values, np.less_equal,order=(5))[0]]['close']
    #plotting local highs for price
    df['max'] = df.iloc[argrelextrema(df.close.values, np.greater_equal,order=5)[0]]['close']

    #oscilator (kinda useless now that i think about it)
    #plotting rsi values at price local low/high
    df['RSImin'] = df.iloc[argrelextrema(df.RSI.values, np.less_equal,order=5)[0]]['RSI']
    #plotting local highs for rsi
    df['RSImax'] = df.iloc[argrelextrema(df.RSI.values, np.greater_equal,order=5)[0]]['RSI']
    #__________________________________________________________#


    find_divergences(df)
    create_plot(df)
    print(df)
    df.to_csv(r'dfCSV.txt', header=None, index=None, sep=',', mode='w+')


def find_divergences(df):
    #ALL TYPES OF DIVERGENCES :#
    #__________________________#
    #regular bullish divergence : price(lower low or equal low) & osci(higher low)
    #hidden bullish divergence : price(higher low) & osci(lower low)
    #regular bearish divergence : price(higher high or equal high) & osci(lower high)
    #hidden bearish divergence : price(lower high) & osci(higher high)
    #__________________________#

    #retrieving all lows into list for BULLISH divs
    #filter all NaNs out of the dataframe then convert to list
    #added BB_MIDDLE.notna() (to wait for correct rsi calculation)
    local_low = df[df['min'].notna() & df['RSI'].notna()& df['BB_MIDDLE'].notna()]
    lldf = pd.DataFrame(local_low, columns= ['min', 'RSI'])
    local_low_list = lldf.values.tolist()

    #print(local_low)
    #iterate through nested list looking for price lower lows and rsi higher lows (neighbours)
    for index, value in enumerate(local_low_list[:-1]):
        for index2 in list(range(index,len(local_low_list)-1)):
            if(local_low_list[index][0]>local_low_list[index2+1][0]):
                if(local_low_list[index][1]<local_low_list[index2+1][1]):
                    if((local_low_list[index][1]!=float(0)) and (local_low_list[index+1][1]!=float(0))):
                        print("regular bullish divergence found @low n°",index+1)
                        print(local_low_list[index],"->")
                        print(local_low_list[index2+1])
            else :
                if(local_low_list[index][1]>local_low_list[index2+1][1]):
                    if((local_low_list[index][1]!=float(0)) and (local_low_list[index+1][1]!=float(0))):
                        print("hidden bullish divergence found @low n°",index+1)
                        print(local_low_list[index],"->")
                        print(local_low_list[index2+1])

    #retrieving all highs into list for BEARISH divs
    local_high = df[df['max'].notna() & df['RSI'].notna()& df['BB_MIDDLE'].notna()]
    lhdf = pd.DataFrame(local_high, columns= ['max', 'RSI'])
    local_high_list = lhdf.values.tolist()
    print(local_high)#purely for testing purposes

    for index, value in enumerate(local_high_list[:-1]):
        for index2 in list(range(index,len(local_high_list)-1)):
            if(local_high_list[index][0]<local_high_list[index2+1][0]):
                if(local_high_list[index][1]>local_high_list[index2+1][1]):
                    if((local_high_list[index][1]!=float(0)) and (local_high_list[index+1][1]!=float(0))):
                        print("regular bearish divergence found @high n°",index+1)
                        print(local_high_list[index],"->")
                        print(local_high_list[index2+1])
            else :
                if(local_high_list[index][1]<local_high_list[index2+1][1]):
                    if((local_high_list[index][1]!=float(0)) and (local_high_list[index+1][1]!=float(0))):
                        print("hidden bearish divergence found @high n°",index+1)
                        print(local_high_list[index],"->")
                        print(local_high_list[index2+1])





valuesforDF()
