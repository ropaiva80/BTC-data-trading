## Historic-Crypto 0.1.6 ##
## An open source Python library for the collection of Historical Cryptocurrency data. ##
## https://pypi.org/project/Historic-Crypto/
## Copy table SQL - https://docs.microsoft.com/en-us/sql/relational-databases/tables/duplicate-tables?view=sql-server-ver15
## C:\Users\ropai\anaconda3\envs\
## conda activate cryptov4-env-nogluonts

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
start_date = '2022-01-07-00-00'
end_date = '2022-03-08-11-00'
new = HistoricalData('SOL-USD',3600,start_date,end_date).retrieve_data()
new = new.reset_index()
new.rename(columns={'index': 'time'}, inplace=True)

new.dropna(inplace=True)
warnings.filterwarnings('ignore') 

from autots import AutoTS
model = AutoTS(forecast_length=8, frequency='infer', ensemble='simple')
model = model.fit(new, date_col='time', value_col='close', id_col=None)

prediction = model.predict()
forecast = prediction.forecast
print(forecast)
df = forecast
df = df.reset_index()
df.rename(columns={'index': 'time'}, inplace=True)
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
	cursor.execute("INSERT INTO SOLANA_v1_COINBASE (DATETIME_PREDICTION,PRICE_PREDICTION,ASSET_NAME,ALGORITHMS,CATEGORY) values(?,?,'SOLANA','AUTOTS_GLUONTS_OFF','HOURLY')", row.time, row.close)
cnxn.commit()
cursor.close()