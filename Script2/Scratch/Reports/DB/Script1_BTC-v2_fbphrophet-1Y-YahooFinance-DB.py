##### 12/28/21 10:47 pm
#####https://medium.com/bitgrit-data-science-publication/ethereum-price-prediction-with-python-3b3805e6e512
#####(downgrade) PS C:\Users\Robson> conda activate time_series

import pandas as pd
import yfinance as yf
from datetime import datetime
from datetime import timedelta
import plotly.graph_objects as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import warnings
import plotly.io as pio
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
pd.options.display.float_format = '${:,.2f}'.format
import plotly.offline as py
import pyodbc


today = datetime.today().strftime('%Y-%m-%d')
start_date = '2016-01-01'
eth_df = yf.download('BTC-USD',start_date, today)
eth_df.tail()

eth_df.isnull().sum()
eth_df.reset_index(inplace=True)
eth_df.columns

df = eth_df[["Date", "Open"]]

new_names = {
    "Date": "ds", 
    "Open": "y",
}
df.rename(columns=new_names, inplace=True)

df.tail()

# plot the open price

x = df["ds"]
y = df["y"]

fig = go.Figure()

fig.add_trace(go.Scatter(x=x, y=y))

fig.update_layout(title="Time series plot of Bitcoin Open Price",legend_title="Merda")

fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(step="all"),
                ]
            )
        ),
        rangeslider=dict(visible=True),
        type="date",
    )
)

m = Prophet(
    interval_width=0.8,daily_seasonality=True,changepoint_prior_scale = 0.8, seasonality_mode='multiplicative', seasonality_prior_scale = 1
)

m.fit(df)

future = m.make_future_dataframe(periods = 365)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

next_day = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

forecast[forecast['ds'] == next_day]['yhat'].item()
m.plot_components(forecast).savefig('Test_BTC.png')
plt.savefig("Test_BTC.png",dpi=300)


#fig = plot_plotly(m, forecast, trend=True, changepoints=True)
#fig.update_layout(title="Bitcoin Open Price - Script1")
#fig.show()


#plt.title('zeca')
#plot_plotly(m, forecast)
#plot_plotly(m, forecast).show()
#plot_components_plotly(m, forecast)
