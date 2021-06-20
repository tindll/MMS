import math
import pandas_datareader as web
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM
import matplotlib.pyplot as plt

plt.style.use('dark_background')
df=pd.read_csv('/testingTF/dfCSV.txt')
print(df)

plt.figure(figsize=(16,8))
plt.title('open Price History')

plt.plot(df['close'])

plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price')

#plt.show() won't work because i'm a terminal only LEGEND.
plt.savefig('/testingTF/plotty_wotty.png')

data = df.filter(['close'])
dataset = data.values

#training the model

train_len = math.ceil(len(dataset)*.7)
print(train_len)

#scale
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)


#create the training data set
#create the scaled training data set
train_data = scaled_data[0:train_len, :]
# x and y train
x_train = []
y_train = []

for i in range(100,len(train_data)):
    x_train.append(train_data[i-100:i,0])
    y_train.append(train_data[i,0])
    if i<=100:
        print(x_train)
        print(y_train)

#convert x and y train for lstm model
x_train,y_train = np.array(x_train),np.array(y_train)

#reshape (lstm needs 3 dimension, but here's it's 2)
x_train = np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))
print(x_train.shape)



#LSTM model
model = Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(LSTM(50,return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

#compile model (improve on loss function; how well model did)
model.compile(optimizer='adam', loss='mean_squared_error')


#train model
model.fit(x_train,y_train,batch_size=1, epochs=1)


#create testing dataset
test_data = scaled_data[train_len-100: , :]
#create data sets x and y
x_test =[]
# y are values that we want the model to predict
y_test =dataset[train_len:,:]

for i in range(100,len(test_data)):
    x_test.append(test_data[i-100:i,0])

# convert data to numpy
x_test = np.array(x_test)

#reshape (2 dim to 3 dim) -- 1 because number of features (close price)
x_test = np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

#get predicted price values; predictions should be identical to y_test dataset
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

#get rmse
rmse = np.sqrt(np.mean(predictions-y_test)**2)
print(rmse)

#plot
train = data[:train_len]
valid = data[train_len:]
valid['Predictions'] = predictions
plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date',fontsize=18)
plt.ylabel('close', fontsize=18)
plt.plot(train['close'])
plt.plot(valid[['close','Predictions']])
plt.legend(['Train','Val','Predictions'],loc='lower right')
plt.savefig('/testingTF/model_plot.png')