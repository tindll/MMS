# **ml_models**
Although I didn't do as much ML as I would have liked, the project still served as a good introduction to machine learning. (Basic concepts & simple implementation)

This file contains everything related to the machine learning side of the project.
Both test.py files use the dataframe created by TA_ALGO.py .

## test1.py
This file is an LSTM based model that tries to predict the closing price of an asset (in this case ETH) based on previous close prices.
What I've learnt through this project on machine learning is that if a model predicts with a very high accuracy%, something's probably wrong.

The approach taken for this model was to try and predict tomorrow's closing price based on the last 100 day closes, hence why the predicted values are so closely correlated to the actual values. However, when actually applied to trading, this model would not make profit.
<br>Although this model may be wrong, it served as a useful stepping stone.

![test1plot](https://github.com/tindll/MMS/blob/main/ml_models/model_plot.png)

## test2.py
This file is a random forest based model that tries to predict whether the close in 10 candles time (in this case 40hours) is higher or lower than the current close.
Unlike the previous model, this one also takes technical indicators into consideration.
This model has a more realistic approach, achieving roughly ~53% correct prediction rate. This could be considerably higher with a bit of tweaking. (better choice of techincal indicators amongst other things)

![test2output](https://github.com/tindll/MMS/blob/main/ml_models/test2ret.PNG)    &emsp;     &emsp;&emsp;                         ![var_corr](https://github.com/tindll/MMS/blob/main/ml_models/variable_correlation_test2.png)
<br>
![test2chart](https://github.com/tindll/MMS/blob/main/ml_models/model2.png)


<br><br>
#### How I'd continue with machine learning : 
To start with, I'd look at more courses, watch more videos, just generally learn more about ML. (coursera, google ML crash course ...)
<br> I'd then try to fix my previous mistakes and make these models better.
<br>
At first, my approach to the problem at hand was wrong, I was thinking about regression based models instead of classification ones.
<br> So I would try different approaches, including something similar to the one in [this paper](https://e-tarjome.com/storage/panel/fileuploads/2019-06-15/1560578401_E11311-e-tarjome.pdf).
<br> And I'd definitely use jupyter notebook instead of running the code on a container.




