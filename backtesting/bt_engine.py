# i want this file to look through trades.json 
# and for each trade i want it to determine if it's a good trade or a bad one
# for this, all trades need an exit condition
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
from binance.client import Client
from finta import TA
from scipy.signal import argrelextrema 



with open('../trades.json','r+') as tradesJSON1:
    data = json.load(tradesJSON1)
    tradeID = len(data['trades'])+1
    tradeID = str(tradeID)
    print(data)