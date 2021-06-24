# ml_models
Although I didn't do as much ML as I would have liked, the project still served as a good introduction to machine learning. (Basic concepts & simple implementation)

This file contains everything related to the machine learning side of the project.

## test1.py
This file is an LSTM based model that tries to predict the closing price of an asset (in this case ETH) based on previous close prices.

Although this model may be wrong in almost every way possible, it served as a useful stepping stone.
![most recent chart](https://github.com/tindll/MMS/blob/main/ml_models/model_plot.png)

###### How to run these files :
https://docs.docker.com/get-started/


1) A python script will create signals when it thinks it's a good time to enter a position (short/long), based on RSI divergences, close above/below bbands, macd crossovers and potentially ichimoku clouds (given a better understanding of clouds).
The python code also produces charts (as seen below) and I would like to make a website that shows all active trades with pertinent information : http://www.zjamsty.com/

2) I would also like to try and make a regression based machine learning AI using tensorflow. (My python code produces a CSV like file (see c:\data\pandas.txt), and thanks to the binance API, I have access to a near unlimited supply of price information, my datasets will be produced thanks to these "CSV" files)

![most recent chart](https://github.com/tindll/mms/blob/main/chart.png)



*List of tasks in progress and to do are under the project tab.*
