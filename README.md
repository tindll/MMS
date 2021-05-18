# MMS - proof of concept
Project as an introduction to algorithmic trading. Despite the name, the sole goal isn't just to turn a profit but to understand how to automize the process of trading.
As I don't want to overcomplexify my trading strategy to start with, I will use simple indicators such as momentum, macd, rsi, bbands (potentially fibonacci
retracements, ATR, Ichimoku Clouds for things such as closing a position). 

1) A python script will create signals when it thinks it's a good time to enter a position (short/long), based on RSI divergences, close above/below bbands, macd crossovers and potentially ichimoku clouds (given a better understanding of clouds).
The python code also produces charts (as seen below) and I would like to make a website that shows all active trades with pertinent information : http://www.zjamsty.com/

2) I would also like to try and make a regression based machine learning AI using tensorflow. (My python code produces a CSV like file (see c:\data\pandas.txt), and thanks to the binance API, I have access to a near unlimited supply of price information, my datasets will be produced thanks to these "CSV" files)

![most recent chart](https://github.com/tindll/mms/blob/main/chart.png)



Currently working on bullish RSI divergences : (currently around 66% are correct) -- needs tweaking -- understatement
ex: "bullish rsi divergence found @low n° 0
[55341.27, 28.6233581015521] ->
[54937.27, 33.13886849423598]
bullish rsi divergence found @low n° 6
[56026.83, 35.85173667301406] ->
[55875.51, 37.22766941713545]
bullish rsi divergence found @low n° 10
[49801.23, 24.515514371037156] ->
[49171.76, 32.624704007384494]
bullish rsi divergence found @low n° 18
[49444.7, 39.2708812295124] ->
[49322.03, 40.24998175626117]
bullish rsi divergence found @low n° 24
[47144.66, 31.33744764904344] ->
[46762.99, 32.73156245229599]
bullish rsi divergence found @low n° 28
[44104.07, 18.841546334527024] ->
[42915.46, 25.684385612563375]"


# TODO - 04/05/21
short term: code a long/short signal

long term: learn more about ML, figuring out tensorflow

# TODO - 28/04/21
figure out an API to use, how to use it

