###(EXCELLENT)###

############################################################################################################################
### Send Report - BTC 1H - Predict
############################################################################################################################

####################################################
# https://pypi.org/project/pretty-html-table/
# 	=> pip install pretty_html_table
# https://pypi.org/project/O365/
# 	=> pip install o365
# 	=> pip install sphinx==2.2.2
# https://o365.github.io/python-o365/latest/api/account.html
# https://github.com/ykorzikowski/python-fritz-office-365-sync/blob/6810fa3d9cd1b1e780e443586f39b758f4a06882/python-fritz-office-365-sync/core.py#L12
# https://github.com/O365/python-o365/issues/167
####################################################

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

### Database connection - Microsoft SQL Server ###

#new - database connection #
server = 'tcp:127.0.0.1'
database = 'Cryptopredict_script2'
username = 'script2'
password = 'C4nd4r0l*'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

## Feed a new dataframe from SQL

df0 = pd.read_sql_query('SELECT * FROM BITCOIN_v1_COINBASE', cnxn)

df1 = pd.read_sql_query('SELECT * FROM BITCOIN_v2_YAHOOFINANCE', cnxn)



#################### Select information block by datetime ####################

#Datetime function to range of select

init_time_now = datetime.now()
datetime1 = init_time_now - timedelta(days = 1)
datetime1 = datetime1.strftime('%Y-%m-%d %H:%M:%S')
datetime2 = init_time_now + timedelta(days = 6)
datetime2 = datetime2.strftime('%Y-%m-%d %H:%M:%S')

mask = (df1['DATETIME_PREDICTION'] >= datetime1) & (df1['DATETIME_PREDICTION'] <= datetime2)
df1.loc[mask]
grouped_prediction = df1.loc[mask]

grouped_prediction_final1 = (grouped_prediction.groupby(['ALGORITHMS', pd.Grouper(key='DATETIME_PREDICTION')]).agg({'PRICE_PREDICTION'}))
grouped_prediction_final1 = grouped_prediction_final1.reset_index()
grouped_prediction_final2 = (grouped_prediction.groupby(['DATETIME_PREDICTION', pd.Grouper(key='ALGORITHMS')]).agg({'PRICE_PREDICTION'}))
grouped_prediction_final2 = grouped_prediction_final2.reset_index()
grouped_prediction_final = pd.concat([grouped_prediction_final2,grouped_prediction_final1])
grouped_prediction_final[grouped_prediction_final["ALGORITHMS"].str.contains("DAILY")==False]


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

###########################################################################################################################
#### notes																							 ##
####mask = (df1['DATETIME_PREDICTION'] >= "2022-05-04 00:00:00") & (df1['DATETIME_PREDICTION'] <= "2022-05-04 23:00:00") ##
###########################################################################################################################