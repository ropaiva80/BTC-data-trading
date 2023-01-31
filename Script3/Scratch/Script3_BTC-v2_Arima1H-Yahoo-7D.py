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

#Datetime settings

end_date = datetime.today()
end_date += timedelta(days=1)
end_date = end_date.strftime('%Y-%m-%d')

init_time_now = datetime.now()
start_date = init_time_now - timedelta(days=6)
start_date = start_date.strftime('%Y-%m-%d')


#Download of dataset

eth_df = yf.download('BTC-USD',start_date, end_date, interval='1M')
eth_df.dropna(inplace=True)
eth_df.reset_index(inplace=True)
eth_df.rename(columns={'index': 'Datetime'}, inplace=True)
eth_df['Datetime'] = eth_df['Datetime'].dt.tz_localize(None)


matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

stock=eth_df
cols = ['High', 'Low', 'Open', 'Volume']
stock.drop(cols, axis=1, inplace=True)
stock = stock.sort_values('Datetime')
stock = stock.groupby('Datetime')['Close'].sum().reset_index()
stock = stock.set_index('Datetime').asfreq('1T')
stock.isnull().sum()
stock = stock.sort_values('Datetime')
stock = stock.groupby('Datetime')['Close'].sum().reset_index()
stock = stock.set_index('Datetime').asfreq('1T')
stock.isnull().sum()
stock.index

decomposition = sm.tsa.seasonal_decompose(stock, model='additive', period=1)

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 5) for x in list(itertools.product(p, d, q))]

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
							  freq='T',
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}1 - AIC:{}'.format(param, param_seasonal, results.aic))     
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

pred = results.get_prediction(start=pd.to_datetime(end_date), dynamic=False)
pred_ci = pred.conf_int()

#final# Producing and visualizing forecasts - 6 hours ahead

pd.options.display.float_format = '${:,.2f}'.format
pred_uc = results.get_forecast(steps=5)
pred_ci = pred_uc.conf_int()
print (pred_uc.predicted_mean)

clock = datetime.now()
print (clock.strftime("%Y-%m-%d %H:%M:%S"))
