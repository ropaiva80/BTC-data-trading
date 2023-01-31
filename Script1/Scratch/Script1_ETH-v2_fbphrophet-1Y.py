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
import plotly.offline as py
import plotly.io as pio
import plotly.express as px
warnings.filterwarnings('ignore')
pd.options.display.float_format = '${:,.2f}'.format


today = datetime.today().strftime('%Y-%m-%d')
start_date = '2017-01-01'
eth_df = yf.download('ETH-USD',start_date, today)
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

fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
        rangeslider=dict(visible=True),
        type="date",
    )
)

m = Prophet(
    ##interval_width=0.4,daily_seasonality=True,changepoint_prior_scale = 0.8, seasonality_mode='multiplicative'
    interval_width=0.8,daily_seasonality=True,changepoint_prior_scale = 0.8, seasonality_mode='multiplicative', seasonality_prior_scale = 1
    
    #### interval_width=0.4,daily_seasonality=True,seasonality_mode='multiplicative',changepoint_prior_scale = 0.1,seasonality_prior_scale = 0.1

)

m.fit(df)

future = m.make_future_dataframe(periods = 365)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

next_day = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

forecast[forecast['ds'] == next_day]['yhat'].item()
fig = plot_plotly(m, forecast, trend=True, changepoints=True)
fig.update_layout(title="Ethereum Open Price - Script1")
fig.write_html("C:\Python\Crypto\Script1\Scratch\Reports\EthereumOpenPrice - Script1.html")


#fig = plot_plotly(m, forecast, trend=True, changepoints=True)
#fig.update_layout(title="Ethereum Open Price - Script1")
#fig.show()


#plot_plotly(m, forecast)
#plot_plotly(m, forecast).show()
#plot_components_plotly(m, forecast)
