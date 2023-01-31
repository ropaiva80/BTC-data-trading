
# ==========================================================================================
# https://github.com/hima888/Stock-market-forecasting/blob/master/Arima%20stock%20market%20forecasting%20.ipynb
# Stock-market-forecasting/Arima stock market forecasting .ipynb
# hima888 Latest commit 80e180d on Apr 18, 2020
# ==========================================================================================
#Prediction for 24HS / per day #

import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
import statsmodels.api as sm
import matplotlib
import warnings
import pyodbc
import yfinance as yf
from pylab import rcParams
from datetime import datetime
from datetime import timedelta


matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'


####today = '2022-03-20'
today = datetime.today().strftime('%Y-%m-%d')
start_date = '2017-01-01'
eth_df = yf.download('ETH-USD',start_date, today)
stock=eth_df
stock.head()

#stock['Date']=pd.to_datetime(df.Date,format='%Y%m%d', errors='ignore')
stock.Date = pd.to_datetime(stock.Date, format='%Y%m%d', errors='ignore')

cols = ['High', 'Low', 'Open', 'Volume', 'Adj Close']
stock.drop(cols, axis=1, inplace=True)
stock = stock.sort_values('Date')
stock.isnull().sum()
stock = stock.groupby('Date')['Close'].sum().reset_index()
stock = stock.set_index('Date')
stock.index

rcParams['figure.figsize'] = 18, 8
decomposition = sm.tsa.seasonal_decompose(stock, model='additive')
##fig = decomposition.plot()
##plt.show()

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 48) for x in list(itertools.product(p, d, q))]

print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))


l_param = []
l_param_seasonal=[]
l_results_aic=[]
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(stock,
					    freq='D',
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}48 - AIC:{}'.format(param, param_seasonal, results.aic))     
            l_param.append(param)
            l_param_seasonal.append(param_seasonal)
            l_results_aic.append(results.aic)
        except:
            continue
	
minimum=l_results_aic[0]

for i in l_results_aic[1:]:
    if i < minimum: 
        minimum = i

i=l_results_aic.index(minimum)


mod = sm.tsa.statespace.SARIMAX(stock,
                                order=l_param[i],
                                seasonal_order=l_param_seasonal[i],
                                enforce_stationarity=False,
                                enforce_invertibility=False)

results = mod.fit()
print(results.summary().tables[1])



pred = results.get_prediction(start=pd.to_datetime('2021-12-31'), dynamic=False)
pred_ci = pred.conf_int()

ax = stock['2020':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)

ax.set_xlabel('Date')
ax.set_ylabel('close price')
##plt.legend()
##plt.show()


#final# Producing and visualizing forecasts - 7 days ahead

pred_uc = results.get_forecast(steps=7)
pred_ci = pred_uc.conf_int()

ax = stock.plot(label='observed', figsize=(14, 7))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('close price')

plt.legend()
plt.show()

print (pred_uc.predicted_mean)