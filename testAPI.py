import os
import mplfinance as mpf
import pandas as pd
import numpy as np
import datetime
import sys
import urllib.request, json 
from binance.client import Client
from finta import TA
from scipy.signal import argrelextrema #for local highs/lows

#checking that we have 3 arguments (the validity of the arguments is tested later)
if(len(sys.argv)!=3):
    print("testAPI.py was called with the wrong amount of arguments")
    sys.exit()

#getting symbol and timeframe from command line
symbol = sys.argv[1]
timeframe = sys.argv[2]



print(symbol,timeframe)

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

#print(client.get_top_long_short_positions('BTCUSDT','15m'))

# get latest price from Binance API
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
# print full output (dictionary)
print(btc_price)

begin_time = datetime.datetime.now() # want an idea of execution time
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
    mpf.plot(df, type='candle', axtitle = "BTCUSDT 15M (1D)", xrotation=20, datetime_format=' %A, %d-%m-%Y', savefig='chart.png', volume = True, volume_panel=2, style = s,addplot=ap0, fill_between=dict(y1=df['BB_LOWER'].values, y2=df['BB_UPPER'].values, alpha=0.15))

def valuesforDF():
    #fills dataframe with information : open, close, etc... & rsi, macd, bbands
    open,high,low,close,time,pandasdti,volume = [],[],[],[],[],[],[]
    for kline in client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "3 days ago UTC"):
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

    #dataframe information for divergences (find_divergences())
    # finds local highs/ local lows and filters noise
    #__________________________________________________________#
    #plotting local lows for price
    df['min'] = df.iloc[argrelextrema(df.close.values, np.less_equal,order=(5))[0]]['close']
    #plotting local highs for price
    df['max'] = df.iloc[argrelextrema(df.close.values, np.greater_equal,order=(5))[0]]['close']

    #plotting rsi values at price local low/high
    df['RSImin'] = df.iloc[argrelextrema(df.RSI.values, np.less_equal,order=5)[0]]['RSI']
    #plotting local highs for rsi
    df['RSImax'] = df.iloc[argrelextrema(df.RSI.values, np.greater_equal,order=5)[0]]['RSI']
    #__________________________________________________________#


    #calling to indictor functions
    find_divergences(df)
    #find_macd_signalCrossovers(df)
    dmi_crossover(df)
    
    #call to the function that creates the graph
    create_plot(df)

    #creating CSV file from the dataframe
    df.to_csv(r'dfCSV.txt', header=None, index=None, sep=',', mode='w+')

#this function and macd crossovers could just be one function
def dmi_crossover(df):
    dmi_cross = df[['ADX','DMIp','DMIm','close']]
    dmi_cross = dmi_cross[(dmi_cross['ADX']>25)  & (dmi_cross['ADX']<100) & (dmi_cross['ADX'].notna()) ] #filtering dataframe where ADX is >25 ; only look for positions if trend isn't weak
    print(dmi_cross)
    dmicrossover = '' #declaring here because of first iteration
    for row in dmi_cross.itertuples(): #ugly code, need to find a better way to do this
        if(row.DMIp>row.DMIm):
            if(dmicrossover=='BELOW'): #filtering signals with %BB
                print("potential bullish trend reversal @ ",row.Index,'@', row.close)
            dmicrossover = 'ABOVE'
        else : 
            if(dmicrossover=='ABOVE'): #filtering signals with %BB
                print("potential bearish trend reversal @ ",row.Index,'@', row.close)
            dmicrossover = 'BELOW'

def find_macd_signalCrossovers(df):
    #function to find MACD crossovers
    # !! only to be used in combination with another indicator !! & work best in strong trending markets (also it's lagging because ur dealing with MAs) 
    # potential bullish signal: when MACD crosses up over signal line
    # potential bearish signal : when MACD crosses below signal line
    # MACD -> red line on chart   || signal -> orange line on chart
    # note : i want to df_crossovers.loc[(df_crossovers['MACD']==df_crossovers['MACD_signal'])], but i can't because it only keeps hourly macd values and won't find crossovers, might have to iterate through :(
    df_crossovers = df[['MACD','MACD_signal','close']]
    crossover = '' #declaring here because of first iteration
    for row in df_crossovers.itertuples(): #ugly code, need to find a better way to do this
        if(row.MACD>row.MACD_signal):
            if(crossover=='DOWN'): #filtering signals with %BB
                print("bullish crossover @ ",row.Index,'@', row.close)
            crossover = 'UP'
        else : 
            if(crossover=='UP'): #filtering signals with %BB
                print("bearish crossover @ ",row.Index,'@', row.close)
            crossover = 'DOWN'


#find divergences could be generalized to detect divergences on all indicators not just RSI
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

    print(local_low)
    unixTIME_EQ =local_low.index.astype(int) / 10**9
    #print(unixTIME_EQ[1])
    #iterate through nested list looking for price lower lows and rsi higher lows (neighbours)
    for index, value in enumerate(local_low_list[:-1]):
        foundBelowLineRB = False
        foundBelowLineHB = False
        for index2 in list(range(index+1,len(local_low_list)-1)):
            if(local_low_list[index][0]>local_low_list[index2][0]):   #price makes lower low
                if(local_low_list[index][1]<local_low_list[index2][1]): #rsi makes higher low
                        slope = (local_low_list[index2][0]-local_low_list[index][0])/((unixTIME_EQ[index2]-7200)-(unixTIME_EQ[index]-7200)) # substracing 7200 because of time zone differences 7200s=2h=>time difference to GMT aka unix :)
                        y_intercept= local_low_list[index][0] - slope*(unixTIME_EQ[index]-7200)
                        for index3 in range(index+1,index2):
                            if ((local_low_list[index3][0]-(slope*(unixTIME_EQ[index3]-7200)+y_intercept))<0):
                                foundBelowLineRB= True
                        if not foundBelowLineRB:
                            priceDifference = local_low_list[index][0]-local_low_list[index2][0]
                            RSIDifference = local_low_list[index2][1] - local_low_list[index][1]
                            #print("regular bullish divergence found @low n°",index, " to ", index2," // diff : ",priceDifference,",",RSIDifference)
                            #print(local_low_list[index]," -> ",local_low_list[index2])

            if(local_low_list[index][0]<local_low_list[index2][0]) : #price makes higher low
                if(local_low_list[index][1]>local_low_list[index2][1]): #rsi makes lower low
                    slope = (local_low_list[index2][0]-local_low_list[index][0])/((unixTIME_EQ[index2]-7200)-(unixTIME_EQ[index]-7200)) # substracing 7200 because of time zone differences 7200s=2h=timeDiff to GMT aka unix :)
                    y_intercept= local_low_list[index][0] - slope*(unixTIME_EQ[index]-7200)
                    for index4 in range(index+1,index2):
                        if ((local_low_list[index4][0]-(slope*(unixTIME_EQ[index4]-7200)+y_intercept))<0):
                            foundBelowLineHB= True
                    if not foundBelowLineHB:
                        priceDifference = local_low_list[index2][0]-local_low_list[index][0]
                        RSIDifference = local_low_list[index][1] - local_low_list[index2][1]
                        #print("hidden bullish divergence found @low n°",index, " to ", index2," // diff : ",priceDifference,",",RSIDifference)
                        #print(local_low_list[index]," -> ",local_low_list[index2])


    #retrieving all highs into list for BEARISH divs
    local_high = df[df['max'].notna() & df['RSI'].notna()& df['BB_MIDDLE'].notna()]
    lhdf = pd.DataFrame(local_high, columns= ['max', 'RSI'])
    local_high_list = lhdf.values.tolist()
    unixTIME_EQHI =local_high.index.astype(int) / 10**9
    #print(local_high)
    local_highANDlow = df[(df['max'].notna() | df['min'].notna() ) & df['RSI'].notna()& df['BB_MIDDLE'].notna()]
    #print(local_highANDlow)


    for index, value in enumerate(local_high_list[:-1]):
        foundAboveLineRBe = False
        foundAboveLineHBe = False
        for index2 in list(range(index+1,len(local_high_list)-1)):
            #Regular bearish divergence :
            if(local_high_list[index][0]<local_high_list[index2][0]):   #price makes higher high
                if(local_high_list[index][1]>local_high_list[index2][1]): #rsi makes lower high
                        slope = (local_high_list[index2][0]-local_high_list[index][0])/((unixTIME_EQHI[index2]-7200)-(unixTIME_EQHI[index]-7200)) # substracing 7200 because of time zone differences 7200s=2h=>time difference to GMT aka unix :)
                        y_intercept= local_high_list[index][0] - slope*(unixTIME_EQHI[index]-7200)
                        #print(local_low_list[index][0]," to ",local_low_list[index2+1][0])
                        for index3 in range(index+1,index2):
                            if ((local_high_list[index3][0]-(slope*(unixTIME_EQHI[index3]-7200)+y_intercept))>0):
                                foundAboveLineRBe= True
                                #print("the point ",index3, " // ", local_low_list[index3]," // is below the line from", index, " to ",index2)
                                #print((local_low_list[index3][0]-(slope*(unixTIME_EQ[index3]-7200)+y_intercept)))
                                #print("_________________________________")
                        if not foundAboveLineRBe:
                            priceDifference = local_high_list[index2][0]-local_high_list[index][0]
                            RSIDifference = local_high_list[index][1] - local_high_list[index2][1]
                            #print("regular bearish divergence found @high n°",index, " to ", index2," // diff : ",priceDifference,",",RSIDifference)
                            #print(local_high_list[index]," -> ",local_high_list[index2])

            #Hidden bearish divergence :
            if(local_high_list[index][0]>local_high_list[index2][0]) : #price makes lower high
                if(local_high_list[index][1]<local_high_list[index2][1]): #rsi makes higher high
                    slope = (local_high_list[index2][0]-local_high_list[index][0])/((unixTIME_EQHI[index2]-7200)-(unixTIME_EQHI[index]-7200)) # substracing 7200 because of time zone differences 7200s=2h=timeDiff to GMT aka unix :)
                    y_intercept= local_high_list[index][0] - slope*(unixTIME_EQHI[index]-7200)
                    for index4 in range(index+1,index2):
                        if ((local_high_list[index4][0]-(slope*(unixTIME_EQHI[index4]-7200)+y_intercept))>0):
                            foundAboveLineHBe= True
                    if not foundAboveLineHBe:
                        priceDifference = local_high_list[index][0]-local_high_list[index2][0]
                        RSIDifference = local_high_list[index2][1] - local_high_list[index][1]
                        #print("hidden bearish divergence found @high n°",index, " to ", index2," // diff : ",priceDifference,",",RSIDifference)
                        #print(local_high_list[index]," -> ",local_high_list[index2])

valuesforDF()

#def ():




print("")
print("run time: ",datetime.datetime.now() - begin_time) #execution time
