import math
import pandas_datareader as web
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
df=web.DataReader('AAPL',data_source='yahoo', start='2015-01-01',end='2021-05-10')
print(df)
