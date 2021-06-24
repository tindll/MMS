import subprocess
import time

symbols = ["BTCUSDT", "ETHUSDT", "BCHUSDT", "XRPUSDT", "EOSUSDT", "LTCUSDT", "TRXUSDT", "ETCUSDT", "XLMUSDT","LINKUSDT"]
timeframes = ["15m", "1h", "1d"]

for symbol in symbols:
    for times in timeframes:
        if times == "15m":
            subprocess.run(["python3", "testAPI.py",symbol,times,"2"])
            time.sleep(3)

        if times == "1h":
            subprocess.run(["python3", "testAPI.py",symbol,times,"7"])
            time.sleep(3)

        if times == "1d":
            subprocess.run(["python3", "testAPI.py",symbol,times,"100"])    
            time.sleep(3)
