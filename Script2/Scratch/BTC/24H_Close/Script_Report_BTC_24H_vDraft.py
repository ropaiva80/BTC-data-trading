###(EXCELLENT)###

############################################################################################################################
### Send Report - BTC 1H - Predict
############################################################################################################################

########################################################################################################
# https://pypi.org/project/pretty-html-table/
# 	=> pip install pretty_html_table
# https://pypi.org/project/O365/
# 	=> pip install o365
# 	=> pip install sphinx==2.2.2
# https://o365.github.io/python-o365/latest/api/account.html
# https://github.com/ykorzikowski/python-fritz-office-365-sync/blob/6810fa3d9cd1b1e780e443586f39b758f4a06882/python-fritz-office-365-sync/core.py#L12
# https://github.com/O365/python-o365/issues/167
# https://www.datacamp.com/tutorial/for-loops-in-python (excellent)

########################################################################################################

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

### Database connection - Microsoft SQL Server ###

#new - database connection #
server = 'tcp:127.0.0.1'
database = 'Cryptopredict_script2'
username = 'script2'
password = 'C4nd4r0l*'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


#################### Select information block by datetime ####################

# YAHOO Format #
#Datetime function to range of select

init_time_now = datetime.now()
datetime1 = init_time_now - timedelta(days = 1)
datetime1 = datetime1.strftime('%Y-%m-%d')
datetime2 = init_time_now + timedelta(days = 6)
datetime2 = datetime2.strftime('%Y-%m-%d')


#################### Feeding both Dataframe from SQL's Tables ####################

df0 = pd.read_sql_query('SELECT * FROM BITCOIN_v1_COINBASE', cnxn)


query="select * from BITCOIN_v1_COINBASE where DATETIME_PREDICTION >= {datetime1}"


ok => query="select * from BITCOIN_v1_COINBASE where DATETIME_PREDICTION >= '2022-05-12'"

ok => query="select * from BITCOIN_v1_COINBASE where DATETIME_PREDICTION between '2022-05-12' and '2022-05-16'"

ok => query = "select ID, DATETIME_PREDICTION, PRICE_PREDICTION, DATE_CURRENT, ASSET_NAME, ALGORITHMS, CATEGORY FROM BITCOIN_v1_COINBASE where DATETIME_PREDICTION between '+datetime1+' and '+datetime2+'"  

pd.read_sql(query,cnxn)


df1 = pd.read_sql_query('SELECT * FROM BITCOIN_v2_YAHOOFINANCE', cnxn)


##############################################################################################
# 1* First - applying rules in both dataframe at the same time to filter data by datetime range
# 
##############################################################################################

df_list = pd.concat([df0, df1], join='inner')

mask = (df_list['DATETIME_PREDICTION'] >= datetime1) & (df_list['DATETIME_PREDICTION'] <= datetime2)
df_list.loc[mask]
grouped_prediction0 = df_list.loc[mask]
grouped_prediction = grouped_prediction0[grouped_prediction0["CATEGORY"].str.contains("Hourly") == False]



##############################################################################################
# Data preparation to send to HTML (applying mean over all values of data prediction)
# 
##############################################################################################


grouped_prediction_final0 = (grouped_prediction.groupby(['ALGORITHMS', pd.Grouper(key='DATETIME_PREDICTION')]).agg({'PRICE_PREDICTION':'mean'}))
grouped_prediction_final = grouped_prediction_final0.reset_index()


#################### Changing format prices: from raw to currency format ####################

pd.options.display.float_format = '${:,.2f}'.format


#################### HTML ####################
# https://pypi.org/project/pretty-html-table/
# https://pypi.org/project/O365/

from pretty_html_table import build_table
html_table_blue_light = build_table(grouped_prediction_final, 'blue_light')

# Save to html file
with open('pretty_table.html', 'w') as f:
    f.write(html_table_blue_light)

# Compare to the pandas .to_html method:
with open('pandas_table.html', 'w') as f:
    f.write(df.to_html())

#################### Email Token - Azure settings App Definition ####################

from O365 import Account, MSGraphProtocol, FileSystemTokenBackend

scopes = ['https://graph.microsoft.com/Mail.Send','offline_access']
credentials = ('f5424b9d-4c5b-4cd1-b7c2-1920106ea18d', 'nYm8Q~Zw1i8Iue~dcnh2tHcY44lim9O.ofeFEaAQ')

my_protocol = MSGraphProtocol('beta', 'ropaiva80@outlook.com')
token_backend = FileSystemTokenBackend(token_path='C:\Python\Crypto\Outlook_365_Key\O365_Token', token_filename='o365_token')

account = Account(credentials, scopes=scopes, token_backend=token_backend)

##account.authenticate()

#################### Send Email ####################
# creation of function/class in python to send email using o365 library
#################### Send Email ####################

def send_email(account, to, cc, subject, start, body, end):
    m = account.new_message()
    m.to.add(to)
    m.to.add(cc)
    m.subject = subject
    m.body = start + body + end
    m.send()

start = """<html>
                <body>
                    <strong>BTC Prediction Hourly: What is likely to happen?. </strong><br />"""


end = """       </body>
            </html>"""

from pretty_html_table import build_table

html_table_blue_light = build_table(grouped_prediction_final, 'blue_light')

send_email(account
           , 'ropaiva80@outlook.com'
           , 'cesar@rasectech.com'
           , 'BTC Predictive Analytics 1H - (Analysis Likely Outcome)'
           , start
           , html_table_blue_light
           , end)




########################################################## END #######################################################


## ADDITIONALS notes ##
###########################################################################################################################
#### notes																							 ##
####mask = (df1['DATETIME_PREDICTION'] >= "2022-05-04 00:00:00") & (df1['DATETIME_PREDICTION'] <= "2022-05-04 23:00:00") ##
###########################################################################################################################

##############################################################################
# 2* (second) way to do the same thing like above
##############################################################################

### mask = (df0['DATETIME_PREDICTION'] >= datetime1) & (df0['DATETIME_PREDICTION'] <= datetime2)
### df0.loc[mask]
### grouped_prediction0 = df0.loc[mask]

### grouped_prediction0 = grouped_prediction0[grouped_prediction0["CATEGORY"].str.contains("Hourly") == False]

### mask = (df1['DATETIME_PREDICTION'] >= datetime1) & (df1['DATETIME_PREDICTION'] <= datetime2)
### df1.loc[mask]
### grouped_prediction1 = df1.loc[mask]

### grouped_prediction = pd.concat([grouped_prediction0, grouped_prediction1], join='inner')

### for i in df_list:
###    mask = (i['DATETIME_PREDICTION'] >= datetime1) & (i['DATETIME_PREDICTION'] <= datetime2)
###    i.loc[mask]
###    grouped_prediction0 = i.loc[mask]

#############################################################################
