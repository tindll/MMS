***To execute TA_ALGO.py, you will need binance API keys (mine were declared in envrionment variables), as the algorithm depends on the data it gets from the API.***
<br> 
***You will also need to remove the updateJSON_newtrade() function from TA_ALGO.py as it calls another API to upload the json file to the website.***
<br>
***You may also need to download several python libraries & packages such as; 'pandas, mplfinance, numpy, binance.client, finta, sklearn, tensorflow ...'***
<br>
1. execute 'python3 TA_ALGO.py {ticker} {timeframe} {amountDays}'
<br> where {ticker} = 'BTCUSDT', 'ETHUSDT', 'DOGEUSDT'... , {timeframe} = '30m', '1h','1d','1w' ... & {amountDays} = 15,30,50,700...

![image](https://user-images.githubusercontent.com/76219233/123369604-5561cb00-d57e-11eb-9e1f-71f24f79a135.png)
