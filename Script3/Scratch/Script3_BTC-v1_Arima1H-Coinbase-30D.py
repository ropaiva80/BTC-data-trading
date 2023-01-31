import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
import statsmodels as sm
import statsmodels.api as sm
import matplotlib
import warnings
import pyodbc
import yfinance as yf
from pylab import rcParams
from datetime import datetime
from datetime import timedelta
from Historic_Crypto import HistoricalData
from Historic_Crypto import Cryptocurrencies
from Historic_Crypto import LiveCryptoData

###start_date = '2021-12-20-08-00'
###end_date = '2022-04-01-10-00'

init_time_now = datetime.now()
start_date = init_time_now - timedelta(days=30)
start_date = start_date.strftime('%Y-%m-%d-%H-%M')
end_date = datetime.today()
###end_date += timedelta(days=1)
end_date = end_date.strftime('%Y-%m-%d-%H-%M')


eth_df = HistoricalData('BTC-USD',3600,start_date,end_date).retrieve_data()

matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

stock=eth_df
cols = ['high', 'low', 'open', 'volume']
stock.drop(cols, axis=1, inplace=True)
stock = stock.sort_values('time')
stock = stock.groupby('time')['close'].sum().reset_index()
stock = stock.set_index('time').asfreq('H')
stock.isnull().sum()
stock = stock.sort_values('time')
stock = stock.groupby('time')['close'].sum().reset_index()
stock = stock.set_index('time').asfreq('H')
stock.isnull().sum()
stock.index

decomposition = sm.tsa.seasonal_decompose(stock, model='additive')

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 24) for x in list(itertools.product(p, d, q))]

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
							  freq='H',
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}24 - AIC:{}'.format(param, param_seasonal, results.aic))     
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

end_date = datetime.today()
end_date += timedelta(days=1)
end_date = end_date.strftime('%Y-%m-%d')
pred = results.get_prediction(start=pd.to_datetime(end_date), dynamic=False)
pred_ci = pred.conf_int()

#final# Producing and visualizing forecasts - 7 days ahead

pred_uc = results.get_forecast(steps=6)
pred_ci = pred_uc.conf_int()
print (pred_uc.predicted_mean)

clock = datetime.now()
print (clock.strftime("%Y-%m-%d %H:%M:%S"))