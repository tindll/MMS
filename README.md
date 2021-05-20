# MMS - proof of concept
Project as an introduction to algorithmic trading. Despite the name, the sole goal isn't just to turn a profit but to understand how to automize the process of trading.
As I don't want to overcomplexify my trading strategy to start with, I will use simple indicators such as momentum, macd, rsi, bbands (potentially fibonacci
retracements, ATR, Ichimoku Clouds for things such as closing a position). 

1) A python script will create signals when it thinks it's a good time to enter a position (short/long), based on RSI divergences, close above/below bbands, macd crossovers and potentially ichimoku clouds (given a better understanding of clouds).
The python code also produces charts (as seen below) and I would like to make a website that shows all active trades with pertinent information : http://www.zjamsty.com/

2) I would also like to try and make a regression based machine learning AI using tensorflow. (My python code produces a CSV like file (see c:\data\pandas.txt), and thanks to the binance API, I have access to a near unlimited supply of price information, my datasets will be produced thanks to these "CSV" files)

![most recent chart](https://github.com/tindll/mms/blob/main/chart.png)



Currently working on bullish RSI divergences : -- only detects regular bullish divergences for now
ex : bullish rsi divergence found @low n° 1
[3636.38, 17.92666971652281] ->
[3585.69, 29.538189576123784]
bullish rsi divergence found @low n° 7
[3359.09, 24.08129040341977] ->
[3240.13, 28.626237646918014]
bullish rsi divergence found @low n° 8
[3240.13, 28.626237646918014] ->
[3201.7, 33.13677201537374]
bullish rsi divergence found @low n° 11
[2365.18, 13.690155931966459] ->
[2230.9, 29.03983155737761]

# TODO - 04/05/21
short term: code a long/short signal

long term: learn more about ML, figuring out tensorflow

# TODO - 28/04/21
figure out an API to use, how to use it

