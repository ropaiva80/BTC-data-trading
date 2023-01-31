# Crypto Price Prediction with Python
# AskPython
# https://www.askpython.com/python/examples/crypto-price-prediction
# conda activate cryptov2-env

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
start_date = '2020-01-01'
eth_df = yf.download('SOL-USD',start_date, today)
eth_df.dropna(inplace=True)

eth_df.reset_index(inplace=True)
warnings.filterwarnings('ignore')
pd.options.display.float_format = '${:,.2f}'.format

from autots import AutoTS
model = AutoTS(forecast_length=7, frequency='infer', ensemble='simple', drop_data_older_than_periods=150)
model = model.fit(eth_df, date_col='Date', value_col='Close', id_col=None)
 
prediction = model.predict()
forecast = prediction.forecast
model_results = model.results()
validation = model.results("validation")

print("SOLANA-USD Prediction")
print(forecast)

df = forecast

df = df.reset_index()

df.rename(columns={'index': 'Date'}, inplace=True)

df['ID'] = df.index

# Insert Dataframe into SQL Server:
# OLD #
##cnxn = pyodbc.connect(driver='{SQL Server}', host='LAPTOP-P54FQEM9\SQLEXPRESS', database='Cryptopredict_script2',
##                      trusted_connection='tcon', user='robson', password='1980')
##print ("Connection Successfully Established")
##cursor = cnxn.cursor() 

#new - database connection remote#
server = 'tcp:192.168.0.106' 
database = 'Cryptopredict_script2' 
username = 'script2' 
password = 'C4nd4r0l*' 
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

for index, row in df.iterrows():
    cursor.execute("INSERT INTO SOLANA_v2_YAHOOFINANCE (DATETIME_PREDICTION,PRICE_PREDICTION,ASSET_NAME,ALGORITHMS,CATEGORY) values(?,?,'SOLANA','AUTOTS_GLUONTS_7D','DAILY')", row.Date, row.Close)
    cnxn.commit()
cursor.close()

################################# INCREMENT ################
import datetime
now2 = datetime.datetime.now()
print ("Current date and time of this prediction: ")
print (now2.strftime("%Y-%m-%d %H:%M:%S"))
