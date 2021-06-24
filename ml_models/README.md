# **ml_models**
Although I didn't do as much ML as I would have liked, the project still served as a good introduction to machine learning. (Basic concepts & simple implementation)
This file contains everything related to the machine learning side of the project.

## test1.py
This file is an LSTM based model that tries to predict the closing price of an asset (in this case ETH) based on previous close prices.
What I've learnt through this project on machine learning is that if something predicts with a very high accuracy%, something's probably wrong.

The approach taken for this model was to try and predict tomorrow's closing price based on the last 100 day closes, hence why the predicted values are so closely correlated to the actual values. However, when actually applied to trading, this model would not make profit.
Although this model may be wrong, it served as a useful stepping stone.

![most recent chart](https://github.com/tindll/MMS/blob/main/ml_models/model_plot.png)

## test2.py
This file is a random forest based model that tries to predict whether the close in 10 candles time (in this case 40hours) is higher or lower than the current close.
Unlike the previous model, this one also takes technical indicators into consideration.
This model has a more realistic approach, achieving roughly ~53% correct prediction rate. This could be considerably higher with a bit of tweaking. (better choice of techincal indicators)

![most recent chart](https://github.com/tindll/MMS/blob/main/ml_models/test2ret.PNG)

###### How to run these files :
https://docs.docker.com/get-started/


1) A python script will create signals when it thinks it's a good time to enter a position (short/long), based on RSI divergences, close above/below bbands, macd crossovers and potentially ichimoku clouds (given a better understanding of clouds).
The python code also produces charts (as seen below) and I would like to make a website that shows all active trades with pertinent information : http://www.zjamsty.com/

2) I would also like to try and make a regression based machine learning AI using tensorflow. (My python code produces a CSV like file (see c:\data\pandas.txt), and thanks to the binance API, I have access to a near unlimited supply of price information, my datasets will be produced thanks to these "CSV" files)
