import os
import mplfinance as mpf
import pandas as pd
import numpy as np
import datetime
import sys
import urllib.request
import json
import pandas_profiling
import matplotlib.pyplot as plt
from PIL import Image
from binance.client import Client
from finta import TA
from scipy.signal import argrelextrema #for local highs/lows

#checking that we have 3 arguments (the validity of the arguments is tested later)
if(len(sys.argv)!=4):
    print("gatherData.py was called with the wrong amount of arguments")
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
    #OBV = TA.OBV(df)
    #df['OBV'] = OBV

    df['min1'] = df.iloc[argrelextrema(df.close.values, np.less_equal,order=(15))[0]]['close']
    df['max2'] = df.iloc[argrelextrema(df.close.values, np.greater_equal,order=(15))[0]]['close']


    # marking good places to buy and sell for dataset
    #__________________________________________________________#
    #plotting local lows for price
    df['buy'] = df.iloc[argrelextrema(df.close.values, np.less_equal,order=(30))[0]]['close']
    #plotting local highs for price
    df['sell'] = df.iloc[argrelextrema(df.close.values, np.greater_equal,order=(30))[0]]['close']
    #__________________________________________________________#
    
    df.loc[df.buy.notna(), 'buy_sell'] = 1
    df.loc[df.sell.notna(), 'buy_sell'] = -1
    df.loc[df.buy_sell.isnull(), 'buy_sell'] = 0 #needs changing
    df.loc[df.buy.isnull(), 'buy'] = 0
    df.loc[df.sell.isnull(), 'sell'] = 0

    #df = df.drop(['buy', 'sell'], axis=1)
    #df = df.dropna()
    df['div'] = 0
    find_divergences(df)
    df['BBSQ'] = 0
    check_BBsqueeze(df)


    df = df.drop(['min1', 'max2'], axis=1)

    plt.style.use('dark_background')
    plt.figure(figsize=(16,8))
    plt.title('Model')
    plt.xlabel('datetime',fontsize=18)
    plt.ylabel('close', fontsize=18)
    plt.plot(df['close'])
    #plt.plot(df['MACD'])
    #plt.plot(df['MACD_signal'])
    plt.plot(df['close'].loc[df["buy"]!=0],"g^", markersize=6)
    plt.plot(df['close'].loc[df["sell"]!=0],"rv", markersize=6)
    plt.plot(df['close'].loc[df["BBSQ"]==1],"gv", markersize=12)
    plt.plot(df['close'].loc[df["BBSQ"]==1],"g^", markersize=12)
    plt.plot(df['close'].loc[df["BBSQ"]==-1],"rv", markersize=12)
    plt.plot(df['close'].loc[df["BBSQ"]==-1],"r^", markersize=12)
    plt.plot(df['close'].loc[df["div"]==1],"gx", markersize=12)
    plt.plot(df['close'].loc[df["div"]==2],"gx", markersize=12)
    plt.plot(df['close'].loc[df["div"]==3],"rx", markersize=12)
    plt.plot(df['close'].loc[df["div"]==4],"rx", markersize=12)
    plt.savefig('chart4ML.png')
    #creating CSV file from the dataframe
    df = df.dropna()
    df.to_csv(r'dataset.txt', sep=',', mode='w+')
    #profileR = pandas_profiling.ProfileReport(df)
    #profileR.to_file("./report.html")
    print(df)

#def lookForGoodpositions(df):



def find_divergences(df):
    i = 0
    local_low = df[df['min1'].notna() & df['RSI'].notna()& df['BB_MIDDLE'].notna()]
    lldf = pd.DataFrame(local_low, columns= ['min1', 'RSI'])
    local_low_list = lldf.values.tolist()
    unixTIME_EQ =local_low.index.astype(int) / 10**9
    for index, value in enumerate(local_low_list[:-1]):
        foundBelowLineRB = False
        foundBelowLineHB = False
        for index2 in list(range(index+1,len(local_low_list))):
            if(local_low_list[index][0]>local_low_list[index2][0]):   
                if(local_low_list[index][1]<local_low_list[index2][1]):
                        slope = (local_low_list[index2][0]-local_low_list[index][0])/((unixTIME_EQ[index2]-7200)-(unixTIME_EQ[index]-7200)) # substracing 7200 because of time zone differences 7200s=2h=>time difference to GMT aka unix :)
                        y_intercept= local_low_list[index][0] - slope*(unixTIME_EQ[index]-7200)
                        for index3 in range(index+1,index2):
                            if ((local_low_list[index3][0]-(slope*(unixTIME_EQ[index3]-7200)+y_intercept))<0):
                                foundBelowLineRB= True
                        if not foundBelowLineRB:
                            priceDifference = local_low_list[index][0]-local_low_list[index2][0]
                            RSIDifference = local_low_list[index2][1] - local_low_list[index][1] 
                            df.at[local_low.index[index2],'div']=1
                            i+=1
            if(local_low_list[index][0]<local_low_list[index2][0]) :
                if(local_low_list[index][1]>local_low_list[index2][1]):
                    slope = (local_low_list[index2][0]-local_low_list[index][0])/((unixTIME_EQ[index2]-7200)-(unixTIME_EQ[index]-7200)) # substracing 7200 because of time zone differences 7200s=2h=timeDiff to GMT aka unix :)
                    y_intercept= local_low_list[index][0] - slope*(unixTIME_EQ[index]-7200)
                    for index4 in range(index+1,index2):
                        if ((local_low_list[index4][0]-(slope*(unixTIME_EQ[index4]-7200)+y_intercept))<0):
                            foundBelowLineHB= True
                    if not foundBelowLineHB:
                        priceDifference = local_low_list[index2][0]-local_low_list[index][0]
                        RSIDifference = local_low_list[index][1] - local_low_list[index2][1]
                        df.at[local_low.index[index2],'div']=2
                        i+=1

    local_high = df[df['max2'].notna() & df['RSI'].notna()& df['BB_MIDDLE'].notna()]
    lhdf = pd.DataFrame(local_high, columns= ['max2', 'RSI'])
    local_high_list = lhdf.values.tolist()
    unixTIME_EQHI =local_high.index.astype(int) / 10**9
    local_highANDlow = df[(df['max2'].notna() | df['min1'].notna() ) & df['RSI'].notna()& df['BB_MIDDLE'].notna()]

    for index, value in enumerate(local_high_list[:-1]):
        foundAboveLineRBe = False
        foundAboveLineHBe = False
        for index2 in list(range(index+1,len(local_high_list))):
            if(local_high_list[index][0]<local_high_list[index2][0]):
                if(local_high_list[index][1]>local_high_list[index2][1]):
                        slope = (local_high_list[index2][0]-local_high_list[index][0])/((unixTIME_EQHI[index2]-7200)-(unixTIME_EQHI[index]-7200)) # substracing 7200 because of time zone differences 7200s=2h=>time difference to GMT aka unix :)
                        y_intercept= local_high_list[index][0] - slope*(unixTIME_EQHI[index]-7200)
                        for index3 in range(index+1,index2):
                            if ((local_high_list[index3][0]-(slope*(unixTIME_EQHI[index3]-7200)+y_intercept))>0):
                                foundAboveLineRBe= True
                        if not foundAboveLineRBe:
                            priceDifference = local_high_list[index2][0]-local_high_list[index][0]
                            RSIDifference = local_high_list[index][1] - local_high_list[index2][1]
                            df.at[local_high.index[index2],'div']=3
                            i+=1
            if(local_high_list[index][0]>local_high_list[index2][0]) : 
                if(local_high_list[index][1]<local_high_list[index2][1]): 
                    slope = (local_high_list[index2][0]-local_high_list[index][0])/((unixTIME_EQHI[index2]-7200)-(unixTIME_EQHI[index]-7200)) # substracing 7200 because of time zone differences 7200s=2h=timeDiff to GMT aka unix :)
                    y_intercept= local_high_list[index][0] - slope*(unixTIME_EQHI[index]-7200)
                    for index4 in range(index+1,index2):
                        if ((local_high_list[index4][0]-(slope*(unixTIME_EQHI[index4]-7200)+y_intercept))>0):
                            foundAboveLineHBe= True
                    if not foundAboveLineHBe:
                        priceDifference = local_high_list[index][0]-local_high_list[index2][0]
                        RSIDifference = local_high_list[index2][1] - local_high_list[index][1]
                        df.at[local_high.index[index2],'div']=4
                        i+=1

    print(i,"divergences found")

def check_BBsqueeze(df):
    i = 0
    bbwidth = df[df['BBWIDTH'].notna()& df['ADX'].notna()]
    width_avg = bbwidth["BBWIDTH"].mean()
    std = bbwidth['BBWIDTH'].std()
    bbwidth = bbwidth[bbwidth.BBWIDTH < width_avg-1.25*std] 
    #bbwidth = bbwidth[bbwidth.ADX < 30]
    #print(bbwidth.BBWIDTH, bbwidth.ADX)
    #minV = bbwidth['BBWIDTH'].min()
    copies = []
    for row in bbwidth.itertuples():
        #wait for close below or above bband
        for row2 in df[row.Index:].itertuples():
            #sell signal
            if(row2.close<row2.BB_LOWER):
                #avoid repeating signals
                if (copies.count(row2.Index)<1):
                    copies.append(row2.Index)
                    df.at[row2.Index,'BBSQ'] = -1
                    i += 1
                break
            #buy signal     
            if(row2.close>row2.BB_UPPER):
                #avoid repeating signals
                if (copies.count(row2.Index)<1):
                    copies.append(row2.Index)   
                    df.at[row2.Index,'BBSQ'] = 1
                    i += 1
                break
    print(i,"bollinger band squeezes found")


valuesforDF()
