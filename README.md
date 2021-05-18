# MMS - proof of concept
Project as an introduction to algorithmic trading. Despite the name, the sole goal isn't just to turn a profit but to understand how to automize the process of trading.
As I don't want to overcomplexify my trading strategy to start with, I will use simple indicators such as momentum, macd, rsi, bbands (potentially fibonacci
retracements, ATR, Ichimoku Clouds for things such as closing a position). 

1) A python script will create signals when it thinks it's a good time to enter a position (short/long), based on RSI divergences, close above/below bbands, macd crossovers and potentially ichimoku clouds (given a better understanding of clouds).
The python code also produces charts (as seen below) and I would like to make a website that shows all active trades with pertinent information : http://www.zjamsty.com/

2) I would also like to try and make a regression based machine learning AI using tensorflow. (My python code produces a CSV like file (see c:\data\pandas.txt), and thanks to the binance API, I have access to a near unlimited supply of price information, my datasets will be produced thanks to these "CSV" files)

![most recent chart](https://github.com/tindll/mms/blob/main/chart.png)



Currently working on bullish RSI divergences : (currently around 66% are correct) -- needs tweaking -- understatement
ex: "bullish rsi divergence found @low n° 4
[49631.32, 16.75849322418405] ->
[49171.76, 32.62500481708079]
bullish rsi divergence found @low n° 13
[47144.66, 31.33744771493427] ->
[46762.99, 32.73156249726304]
bullish rsi divergence found @low n° 15
[44104.07, 18.84154633029067] ->
[42915.46, 25.68438561217104]

# TODO - 04/05/21
short term: code a long/short signal

long term: learn more about ML, figuring out tensorflow

# TODO - 28/04/21
figure out an API to use, how to use it

