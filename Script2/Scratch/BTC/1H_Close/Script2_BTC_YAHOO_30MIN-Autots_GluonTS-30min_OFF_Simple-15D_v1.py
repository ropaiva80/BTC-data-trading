## Historic-Crypto 0.1.6 ##
## An open source Python library for the collection of Historical Cryptocurrency data. ##
## https://pypi.org/project/Historic-Crypto/
## Copy table SQL - https://docs.microsoft.com/en-us/sql/relational-databases/tables/duplicate-tables?view=sql-server-ver15
## C:\Users\ropai\anaconda3\envs\
## conda activate cryptov2-37

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
import pytz

#Datetime settings

today = datetime.today()
today += timedelta(days=1)
today = today.strftime('%Y-%m-%d')

init_time_now = datetime.now()
start_date = init_time_now - timedelta(days=15)
start_date = start_date.strftime('%Y-%m-%d')

#Download of dataset
print ("Caution: Yahoo timezone set for UTC Time -7:00")
eth_df = yf.download('BTC-USD',start_date, today, interval='30m')
eth_df.dropna(inplace=True)
eth_df.reset_index(inplace=True)
eth_df.rename(columns={'index': 'Datetime'}, inplace=True)
eth_df['Datetime'] = eth_df['Datetime'].dt.tz_localize(None)

warnings.filterwarnings('ignore')
pd.options.display.float_format = '${:,.2f}'.format


from autots import AutoTS
model = AutoTS(forecast_length=6, frequency='infer', ensemble='simple')
model = model.fit(eth_df, date_col='Datetime', value_col='Close', id_col=None)


prediction = model.predict()
forecast = prediction.forecast
print(forecast)

df = forecast
df = df.reset_index()
df.rename(columns={'index': 'time'}, inplace=True)
df['ID'] = df.index
df['difference'] = df['Close'].diff()
df['difference'] = df['difference'].fillna(0)
print ("Caution: Yahoo timezone set for UTC Time -7:00")
print(df)

#new - database connection remote#
server = 'tcp:127.0.0.1'   
database = 'Cryptopredict_script2' 
username = 'script2' 
password = 'C4nd4r0l*' 
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

for index, row in df.iterrows():
    cursor.execute("INSERT INTO BITCOIN_v2_YAHOOFINANCE (DATETIME_PREDICTION,PRICE_PREDICTION,DIFFERENCE,ASSET_NAME,ALGORITHMS,CATEGORY) values(?,?,?,'BTC','YHooAG-off_YH-S-15D','Hourly')", row.time, row.Close, row.difference)
    cnxn.commit()
cursor.close()

clock = datetime.now()
print (clock.strftime("%Y-%m-%d %H:%M:%S"))