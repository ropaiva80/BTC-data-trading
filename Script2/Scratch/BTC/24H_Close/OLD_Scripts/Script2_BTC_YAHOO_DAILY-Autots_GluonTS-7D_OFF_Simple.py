# Crypto Price Prediction with Python
# AskPython
# https://www.askpython.com/python/examples/crypto-price-prediction
# conda activate cryptov2-37

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from seaborn import regression
sns.set()
plt.style.use('seaborn-whitegrid')
from datetime import datetime
from datetime import timedelta
import warnings
import pyodbc


today = datetime.today().strftime('%Y-%m-%d')
start_date = '2016-01-01'
eth_df = yf.download('BTC-USD',start_date, today)
eth_df.dropna(inplace=True)

eth_df.reset_index(inplace=True)
warnings.filterwarnings('ignore')
pd.options.display.float_format = '${:,.2f}'.format

from autots import AutoTS
model = AutoTS(forecast_length=7, frequency='infer', ensemble='simple', drop_data_older_than_periods=900")
model = model.fit(eth_df, date_col='Date', value_col='Close', id_col=None)
 
prediction = model.predict()
forecast = prediction.forecast
model_results = model.results()
validation = model.results("validation")

print("BTC-USD Prediction")
print(forecast)

df = forecast

df = df.reset_index()

df.rename(columns={'index': 'Date'}, inplace=True)

df['ID'] = df.index 

#new - database connection remote#
server = 'tcp:127.0.0.1' 
database = 'Cryptopredict_script2' 
username = 'script2' 
password = 'C4nd4r0l*' 
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

for index, row in df.iterrows():
    cursor.execute("INSERT INTO BITCOIN_v2_YAHOOFINANCE (DATETIME_PREDICTION,PRICE_PREDICTION,ASSET_NAME,ALGORITHMS,CATEGORY) values(?,?,'BTC','AUTOTS_GLUONTS-OFF_7D_Yahoo_Simple','DAILY')", row.Date, row.Close)
    cnxn.commit()
cursor.close()