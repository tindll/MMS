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
from ftplib import FTP #ftp for json file

with open('testtrades.json','w') as ttjson:
    json.dump({'trades': []},ttjson)



tradeID = 0
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

#if symbol and timeframe were valid, load short/long ratio information from json file
#getting an idea of where 'big money' has been going for the last ~24 hours
SHORT_LONGjson = json.loads(url.read().decode())
averageRatio = 0.0
ratio_list= [] #for standard deviation calculation
for key in SHORT_LONGjson:
    averageRatio+=float(key['longShortRatio'])
    ratio_list.append(float(key['longShortRatio']))
stDev=(np.std(ratio_list, dtype=np.float64))
averageRatio/=30

if((argrelextrema(np.array(ratio_list), np.greater_equal,order=3)[-1][-1])==29):
    if(ratio_list[29]>averageRatio): # not right, needs changing
        print(symbol+' long/short ratio: high #longs')
elif ((argrelextrema(np.array(ratio_list), np.less_equal,order=3)[-1][-1])==29):
    if(ratio_list[29]<averageRatio):
        print(symbol+' long/short ratio: high #shorts')
else : print(symbol+' long/short ratio: undecided')

# !! need to think about this because argrelextrema will return most recent value sometimes and that's not always a good thing

#testing MACD crossovers
cross_UP = []
cross_DOWN = []

## setting up binance API from environment variables ##
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')
client = Client(api_key, api_secret)

# get balances for futures account
#print(client.futures_account_balance())

# get latest price from Binance API
symbol_price = client.get_symbol_ticker(symbol=symbol)
# print full output (dictionary)
#print(symbol_price)

begin_time = datetime.datetime.now() #for execution time

#get idea of potential support/resistance on binance
#def getOrderBookinfo():

def create_plot(df):
    mc = mpf.make_marketcolors(up='w',down='b')
    s  = mpf.make_mpf_style(marketcolors=mc)
    ap0 = [ mpf.make_addplot(df['BB_UPPER'],color='blue',alpha=0.3), #BBANDS
            mpf.make_addplot(df['BB_LOWER'],color='blue',alpha=0.3), #BBANDS
            mpf.make_addplot(df['BB_MIDDLE'],color='grey'), #BBANDS
            mpf.make_addplot(df["RSI"], panel='lower', color='purple', ylabel="RSI"),
            mpf.make_addplot(df["MACD"], panel=2, color='red', ylabel="MACD"),
            mpf.make_addplot(df["MACD_signal"], panel=2, color='orange')
          ]
    mpf.plot(df, type='candle', axtitle = symbol+" "+timeframe +" ("+amountDays+"D)", xrotation=20, datetime_format=' %H:%M, %d-%m-%Y', savefig='charts/chart'+str(tradeID)+'.png', volume = True, volume_panel=3,addplot=ap0, fill_between=dict(y1=df['BB_LOWER'].values, y2=df['BB_UPPER'].values, alpha=0.15))


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

    #profileR = pandas_profiling.ProfileReport(df)
    #profileR.to_file("./report.html")


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


    #calling to indicator functions:
    find_divergences(df)   #works
    #find_macd_signalCrossovers(df) #works
    #dmi_crossover(df) #needs work
    #find_Flags(df)
    #bbRSI(df)
    #check_BBsqueeze(df) #works

    #call to the function that creates the graph
    create_plot(df)
    print(df)
    #creating CSV file from the dataframe
    df.to_csv(r'testingBT.txt', sep=',', mode='w+')


    #close a  trade when a candle closes above/below bband
    #maybe use ATR as well





def bbRSI(df):
    if(df.RSI[-1]>70 and df.BBp[-1]>0.9):
        print(symbol," is overbought")
    elif(df.RSI[-1]<30 and df.BBp[-1]<0.1):
        print(symbol," is undersold")
    else : print(symbol, "is not currently overbought or oversold on this time frame")

#this function and macd crossovers could just be one function
#also this function isn't working too great
def dmi_crossover(df):
    dmi_cross = df[['ADX','DMIp','DMIm','close']]
    dmi_cross = dmi_cross[(dmi_cross['ADX']>25)  & (dmi_cross['ADX']<100) & (dmi_cross['ADX'].notna()) ] #filtering dataframe where ADX is >25 ; only look for positions if trend isn't weak
    dmicrossover = '' #declaring here because of first iteration
    print(dmi_cross)
    for row in dmi_cross.itertuples(): #ugly code, need to find a better way to do this
        if(row.DMIp>row.DMIm):
            if(dmicrossover=='BELOW'): #should filter signals with %BB
                print("potential bullish trend reversal @ ",row.Index,'@', row.close,tradeID+1)
            dmicrossover = 'ABOVE'
        else :
            if(dmicrossover=='ABOVE'): #should filter signals with %BB
                print("potential bearish trend reversal @ ",row.Index,'@', row.close,tradeID+1)
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
                if(df.index[-5]<row.Index):
                    df.at[row.Index,'MACD_cross'] = 'UP'
                    date = (row.Index).strftime("%m/%d/%Y, %H:%M:%S")
                    updateJSON_newtrade(symbol,"LONG",row.close,"TBD",'10x',date,'Bullish MACD crossover',tradeID+1)
            crossover = 'UP'
        else :
            if(crossover=='UP'): #filtering signals with %BB
                if(df.index[-5]<row.Index):
                    df.at[row.Index,'MACD_cross'] = 'DOWN'
                    date = (row.Index).strftime("%m/%d/%Y, %H:%M:%S")
                    updateJSON_newtrade(symbol,"SHORT",row.close,"TBD",'10x',date,'Bearish MACD crossover',tradeID+1)
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

    #print(local_low)
    unixTIME_EQ =local_low.index.astype(int) / 10**9
    #print(unixTIME_EQ[1])
    #iterate through nested list looking for price lower lows and rsi higher lows (neighbours)
    for index, value in enumerate(local_low_list[:-1]):
        foundBelowLineRB = False
        foundBelowLineHB = False
        for index2 in list(range(index+1,len(local_low_list))):
            if(local_low_list[index][0]>local_low_list[index2][0]):   #price makes lower low
                if(local_low_list[index][1]<local_low_list[index2][1]): #rsi makes higher low
                        slope = (local_low_list[index2][0]-local_low_list[index][0])/((unixTIME_EQ[index2]-7200)-(unixTIME_EQ[index]-7200)) # substracing 7200 because of time zone differences 7200s=2h=>time difference to GMT aka unix :)
                        y_intercept= local_low_list[index][0] - slope*(unixTIME_EQ[index]-7200)
                        for index3 in range(index+1,index2):
                            if ((local_low_list[index3][0]-(slope*(unixTIME_EQ[index3]-7200)+y_intercept))<0):
                                foundBelowLineRB= True
                        if not foundBelowLineRB:
                            date = str(local_low.index[index2])
                            tradeID=+1
                            updateJSON_newtrade(symbol,"LONG",local_low_list[index2][0],"TBD",'10x',date,'Regular Bullish divergence found',tradeID)
                            #print("recent regular bullish divergence found")
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
                        date = str(local_low.index[index2])
                        tradeID=+1
                        updateJSON_newtrade(symbol,"LONG",local_low_list[index2][0],"TBD",'10x',date,'Hidden Bullish divergence found',tradeID)
                        #print("recent hidden bullish divergence found")
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
        for index2 in list(range(index+1,len(local_high_list))):
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
                            date = str(local_high.index[index2])
                            tradeID=+1
                            updateJSON_newtrade(symbol,"SHORT",local_high_list[index2][0],"TBD",'10x',date,'Regular Bearish divergence found',tradeID)
                            #print("recent regular bearish divergence found")
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
                        date = str(local_high.index[index2])
                        tradeID=+1
                        updateJSON_newtrade(symbol,"SHORT",local_high_list[index2][0],"TBD",'10x',date,'Hidden Bearish divergence found',tradeID)
                        #print("recent hidden bearish divergence found")
                        #print("hidden bearish divergence found @high n°",index, " to ", index2," // diff : ",priceDifference,",",RSIDifference)
                        #print(local_high_list[index]," -> ",local_high_list[index2])




#def patternRecognition (df): # !! meant for higher timeframes only !!
#function that looks for chart patterns
#
#  note : (stop loss should be set at lowest point of the triangle)
# 1. Continuation Chart Patterns
        #Symmetrical triangle
        #comprised of LHs & HLs, a symmetrical triangle is a continuation pattern
        #this function identifies the trend and tries to find these patterns forming
        #and then creates a buy signal on the 3rd low
        #stop loss should be set at the 1st low
        #!!check volume to make sure!!



# bollinger band squeezes:
# long when bbwidth is low and candle closes above upper bollinger band -- try to ride upwards trend
    #close when ADX > 45

# short when bbwidth is low and candle closes below lower bollinger band
def check_BBsqueeze(df):
    bbwidth = df[df['BBWIDTH'].notna()& df['ADX'].notna()]
    width_avg = bbwidth["BBWIDTH"].mean()
    std = bbwidth['BBWIDTH'].std()
    bbwidth = bbwidth[bbwidth.BBWIDTH < width_avg-1.25*std]
    #bbwidth = bbwidth[bbwidth.ADX < 30]
    #print(bbwidth.BBWIDTH, bbwidth.ADX)
    #minV = bbwidth['BBWIDTH'].min()
    copies = []
    for row in bbwidth.itertuples():
        if (df.index[-10]<row.Index):
            #wait for close below or above bband
            for row2 in df[row.Index:].itertuples():
                #sell signal
                if(row2.close<row2.BB_LOWER):
                    #avoid repeating signals
                    if (copies.count(row2.Index)<1):
                        copies.append(row2.Index)
                        date = str(row2.Index)
                        tradeID=+1
                        updateJSON_newtrade(symbol,"SHORT",row2.close,"close when ADX>40",'10x',date,'Bollinger band squeeze',tradeID)
                    break
                #buy signal
                if(row2.close>row2.BB_UPPER):
                    #avoid repeating signals
                    if (copies.count(row2.Index)<1):
                        copies.append(row2.Index)
                        date = str(row2.Index)
                        tradeID=+1
                        updateJSON_newtrade(symbol,"LONG",row2.close,"close when ADX>40",'10x',date,'Bollinger band squeeze',tradeID)
                    break



#def find_Flags(df):
    #Bull flags
    #comprised of LHs & LLs, a bull flag is a continuation pattern
    #this function identifies the trend and tries to find these patterns forming
    #check impusle move up, if EMA




    #Bear flags
    #comprised of HHs & LHs, a bear flag is a continuation pattern
    #this function identifies the trend and tries to find these patters forming
    #check impusle move down, if EMA

# 2. Reversal Chart Patterns
        #Head and shoulders
        #Slightly more complicated than the previous patterns,
        #The Head & Shoulders pattern is characterized by an uptrend;
        #where the highest high in the uptrend forms the left shoulder
        #where the next high, which is a higher high, forms the head
        #where the next high, which is a lower high, forms the right shoulder
        #the neckline is formed as a line of the lows between both shoulders and the head
        #a position should be entered at the break of the neckline

# 3. Double tops/triple top/ bottom


def updateJSON_newtrade(symbol,positionType,openPrice,close,leverage,Date,tradeReason,trade_ID):
    with open('testtrades.json','r+') as tradesJSON:
        data = json.load(tradesJSON)
        newTRADE = {
            "tradeID": trade_ID,
            "symbol": symbol,
            "positionType": positionType,
            "open$": openPrice,
            "close$": close,
            "leverageX": leverage,
            "Date": Date,
            "tradeReason": tradeReason,
            "chartID": trade_ID
            }
        data['trades'].append(newTRADE)
        tradesJSON.seek(0)
        json.dump(data, tradesJSON, indent = 4)
        tradesJSON.close()
        #print(ftp.getwelcome())
        #ftp.retrlines('LIST')

valuesforDF()


df=pd.read_csv('testingBT.txt')
df = df.set_index('datetime')
LONG_trades,SHORT_trades = [],[]
with open('testtrades.json','r+') as ttjson:
    data = json.load(ttjson)
    for trade in data['trades']:
        if (trade['tradeReason']=="Hidden Bullish divergence found"):
            LONG_trades.append(trade)
        elif (trade['tradeReason']=="Hidden Bearish divergence found"):
            SHORT_trades.append(trade)
for trade in LONG_trades:
    openP = trade['open$']
    date = datetime.datetime.strptime(trade['Date'],'%Y-%m-%d %H:%M:%S')
    print(date)
    print(type(date))
    print(df.loc[date])
    #dft = df.loc[date:]
    #print(dft)
    #day = datetime.datetime.strptime(trade['Date'],"%m/%d/%Y, %H:%M:%S")
    #print(df.loc[datetime.datetime(trade['Date'])])
    #print(datetime.datetime(trade['Date']))

#for trade in SHORT_trades:





print("run time: ",datetime.datetime.now() - begin_time) #execution time

