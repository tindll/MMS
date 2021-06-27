import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

df=pd.read_csv('/testingTF/dataset.txt')

plt.style.use('dark_background')
plt.figure(figsize=(10,6))
plt.title('BTCUSDT 1H-30D')
plt.plot(df['close'])
plt.xlabel('Date',fontsize=18)
plt.ylabel('close$')
plt.savefig('/testingTF/model3.png')

dataset_length = df.shape[0]
split = int(dataset_length * 0.75) # 75/25 split

X = df[['open', 'high', 'low', 'close', 'volume', 'BB_MIDDLE',
        'MACD', 'MACD_signal', 'RSI', 'BBp',
       'ADX', 'DMIp', 'DMIm', 'STOCH_K', 'STOCH_D','BBSQ','div']] 

Y = np.where(df['close'].shift(-24) > df['close'], 1, -1)

X_train, X_test = X[:split], X[split:]
y_train, y_test = Y[:split], Y[split:]

random_forestC = RandomForestClassifier(n_estimators=100,random_state=5)
model = random_forestC.fit(X_train, y_train)
print('Accuracy (%): ', accuracy_score(y_test, model.predict(X_test), normalize=True)*100.0)

report = classification_report(y_test, model.predict(X_test))
print(report)
