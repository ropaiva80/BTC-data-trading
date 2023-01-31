## Historic-Crypto 0.1.6 ##
## An open source Python library for the collection of Historical Cryptocurrency data. ##
## https://pypi.org/project/Historic-Crypto/
## Copy table SQL - https://docs.microsoft.com/en-us/sql/relational-databases/tables/duplicate-tables?view=sql-server-ver15
## C:\Users\ropai\anaconda3\envs\
## conda activate cryptov0-env

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from seaborn import regression
sns.set()
plt.style.use('seaborn-whitegrid')
from datetime import datetime
from datetime import timedelta
import warnings
import pyodbc
from Historic_Crypto import HistoricalData
from Historic_Crypto import Cryptocurrencies
from Historic_Crypto import LiveCryptoData

today = datetime.today().strftime('%Y-%m-%d-%H-%M')
init_time_now = datetime.now()
start_date = init_time_now - timedelta(days = 700)
start_date = start_date.strftime('%Y-%m-%d-%H-%M')
end_date = (today)
new = HistoricalData('BTC-USD',86400,start_date,end_date).retrieve_data()
new = new.reset_index()
new.rename(columns={'time': 'date'}, inplace=True)
new.dropna(inplace=True)
warnings.filterwarnings('ignore')


from autots import AutoTS, load_daily
#####model = AutoTS(forecast_length=8, frequency='infer', ensemble='simple')
model = AutoTS(forecast_length=7, frequency='infer', ensemble='simple')
model = model.fit(new, date_col='date', value_col='close', id_col=None)

prediction = model.predict()
forecast = prediction.forecast
validation = model.results("validation")
print(forecast)
df = forecast
df = df.reset_index()
df.rename(columns={'index': 'time'}, inplace=True)
df['ID'] = df.index

#new - database connection remote#
server = 'tcp:127.0.0.1' 
database = 'Cryptopredict_script2' 
username = 'script2' 
password = 'C4nd4r0l*' 
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

for index, row in df.iterrows():
	cursor.execute("INSERT INTO BITCOIN_v1_COINBASE (DATETIME_PREDICTION,PRICE_PREDICTION,ASSET_NAME,ALGORITHMS,CATEGORY) values(?,?,'BTC','CAG-on_CB-S-DAILY-700D','DAILY')", row.time, row.close)
cnxn.commit()
cursor.close()