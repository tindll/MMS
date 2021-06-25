# **MMS**
- ### General Statements:
   Although it would be unfair to still call this a proof of concept, this project is still unfinished. I undoubtedly intend on continuing it.      
   
      
   The goal for this project wasn't to make an algorithm capable of making a profit, despite the name, but more so as an introduction to the automation
   of trading and machine learning. In hindsight, I may have set my expectations too high given the amount of time I invested in the project, seeing as 
   either of the two subjects

Project as an introduction to algorithmic trading. Despite the name, the sole goal isn't just to turn a profit but to understand how to automize the process of trading.
As I don't want to overcomplexify my trading strategy to start with, I will use simple indicators such as momentum, macd, rsi, bbands (potentially fibonacci
retracements, ATR, Ichimoku Clouds). 

- ### Simplified rundown:

   1. 'TA_algo.py' connects to Binance's API. It retrieves OHLC information from the API, then calls functions from various different python libraries such as pandas,      mplfinance and finta. Thanks to these libraries, the algorithm produces charts, like the one below, based on dataframes containing the OHLC data.
   
   2)Several functions, like 'find_macd_signalCrossovers(df)' & 'find_divergences(df)', are then called on the dataframe to analyze the data and to find potential          positions.

![most recent chart](https://github.com/tindll/mms/blob/main/chart.png)

1) A python script will create signals when it thinks it's a good time to enter a position (short/long), based on RSI divergences, close above/below bbands, macd crossovers and potentially ichimoku clouds (given a better understanding of clouds).
The python code also produces charts (as seen below) and I would like to make a website that shows all active trades with pertinent information : http://www.zjamsty.com/

2) I would also like to try and make a regression based machine learning AI using tensorflow. (My python code produces a CSV like file (see c:\data\pandas.txt), and thanks to the binance API, I have access to a near unlimited supply of price information, my datasets will be produced thanks to these "CSV" files)





*List of tasks in progress and to do are under the project tab.*

