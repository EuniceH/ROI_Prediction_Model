#EH: Load libraries

import os
from sqlite3 import apilevel
from sys import api_version
import streamlit as st
import pandas as pd
#import hvplot.pandas
#from pathlib import Path
import matplotlib.pyplot as plt     
from dotenv import load_dotenv
import requests
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import hvplot.pandas
import holoviews as hv
from PIL import Image
from lr_model_binary import *
from gbtc import *
# from tsf_roi import close_price
# from tsf_roi import fix_data
# from tsf_roi import tsf_table
from nn_predict import *
# from fbprophet import Prophet
# from tsf_roi import *


#EH: load env file
load_dotenv()

#EH:  check alpha key

alpha_api_key=os.getenv('ALPHA_API_KEY')

#EH: import stock pool list

stockpool_list_df=pd.read_csv(
    "Resources/sector_list_v2.txt",
    sep=';'
)

#EH: Rename column
stockpool_list_df.rename(columns={'Ticker':'ticker'},inplace=True)

sector_list=['Consumer Non-Durables',
 'Electronic Technology',
 'Finance',
 'Health Technology',
 'Process Industries',
 'Producer Manufacturing',
 'Technology Services',
 'Utilities']

 #EH: add column to join company name with ticker

stockpool_list_df['Company_Ticker']=stockpool_list_df['Company']+' ('+stockpool_list_df['ticker']+')'

#TB
# Web page name
st.title("Machine Learning Model Comparison")
st.write("The goal of this project is to predict, evaluate and backtest quarterly ROI. Working with S&P 500  financial statements, we selected cash flow statements, and EPS, and economic indicators like inflation rate and we aim to prognoze quarterly ROI.")
# st.image(Image.open('Resources/title_photo.png'))
st.markdown('---')

# Fist part of sidebar
st.sidebar.markdown("# Quarterly ROI% Predictor")

# EH:  get select sector

select_sector = st.sidebar.selectbox('Please select one sector:',
      list(sector_list))


st.sidebar.success(select_sector)


#EH: get select ticker

select_ticker = st.sidebar.selectbox('Please select one ticker:',
      list(stockpool_list_df[stockpool_list_df['Sector']==select_sector]['Company_Ticker']))



st.sidebar.success(select_ticker)


select_ticker=stockpool_list_df[stockpool_list_df['Company_Ticker']==select_ticker]['ticker']
select_ticker=select_ticker.values


#Creating the predict button
st.sidebar.button("Predict")

#EH:  create stock close price df from Alpha data

def close_price(stock, api, days_of_record):
    data_url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+stock +"&outputsize=full&apikey="+api
    r = requests.get(data_url[0])
    data = r.json()
    df=pd.DataFrame(data['Time Series (Daily)']).T.rename(columns={'1. open':'open','2. high':'high','3. low':'low','4. close':'close','5. volume':'volume'})
    df=df.reset_index()

    df=df.set_index('index')
    df.index.name='date'
    df.index=pd.to_datetime(df.index)
    
    df['close']=df['close'].astype('float64')
    df=df.iloc[:days_of_record]
    df['daily_change']=df['close'].pct_change(periods=-1)  
    df=df.dropna()
    return df
    

#EH:  
stock_df=close_price(select_ticker,alpha_api_key,2000)


# fig = go.Figure(data=go.Scatter(x=stock_df.index,y=stock_df['Close'], mode='lines'))
# fig.show()

# fig2 = make_subplots(specs=[[{"secondary_y": True}]])
# fig2.add_trace(go.Scatter(x=stock_df.index,y=stock_df['Close'],name='Price'),secondary_y=False)
# fig2.add_trace(go.Bar(x=stock_df.index,y=stock_df['Volume'],name='Volume'),secondary_y=True)
# fig2.show()


#EH: Display Linear Regression model evaluation reports
with st.expander(f'Logistic Regression Prediction Evaluation For {select_sector}:'):
      output1,output2=evaluate_plot(select_sector)
      table_output1=pd.DataFrame(output1)
      st.table(table_output1)
      st.write(f"The score for Logistic Regression Model is {output2}")
      st.image(f"Resources/lr_{select_sector}.png")

#EH: Display GBTC model evaluation reports
with st.expander(f'Gradient Boosted Prediction Evaluation For {select_sector}:'):
      st.table(run_model(select_sector))
      


#EH: Display NN model evaluation reports

nn_df, nn_plot=nn_predict(select_sector,select_ticker[0])

with st.expander(f"Neural Network actual vs prediction ROI% Table -{select_ticker[0]}"):
      st.dataframe(nn_df,width=1500,height=500)

with st.expander(f"Neural Network actual vs prediction Cumulative ROI% -{select_ticker[0]}"):
      st.write(hv.render(nn_plot,backend='bokeh'))

#EH: Display TSF model evaluation reports
# with st.expander(f'Time Series Forcasting(Prophet) Evaluation For {select_ticker}:'):
#      # st.write(import_data(select_ticker))
#       # st.write(close_price(select_ticker,alpha_api_key))
#       # st.write(fix_data(select_ticker))
#       # st.table(tsf_table(select_ticker))


#       # st.write(table(prophet_df))
#       # st.write(compare(prophet_df))
#       #st.image(f"Resources/TSF_JPM.png")
#       tsf_close=tsf_close_price(select_ticker,alpha_api_key)
#       prophet_df=prophet_df_create(tsf_close)
#       tsf_compare_plot=forecast(prophet_df,select_ticker)

#       st.write(hv.render(tsf_compare_plot,backend='bokeh'))




#EH: dispaly daily percentage change
with st.expander('Daily Percentage Chart'):
  daily_change_chart=stock_df.loc[:,'daily_change'].hvplot(kind='line',width=650,height=400,ylabel='daily_change',xlabel='Date',title='Daily Percentage Chart')

  st.write(hv.render(daily_change_chart,backend='bokeh'))


# EH:  get inflation

inflation_url='https://www.alphavantage.co/query?function=INFLATION_EXPECTATION&apikey='+ alpha_api_key
r= requests.get(inflation_url)
data = r.json()
inflation=pd.DataFrame()
for num in range(len(data['data'])):

    inflation_df=pd.DataFrame(data['data'][num],index=['date','value'])
    inflation_df=inflation_df.iloc[0]
    inflation=inflation.append(inflation_df)

#EH: update value to float
inflation['value']=inflation['value'].astype('float64')

#EH: inflation df for chart

inflation_date=inflation.set_index('date')
inflation_date.index=pd.to_datetime(inflation_date.index)

#EH: dispaly inflation chart on streamlit
with st.expander('Inflation Chart'):
  inflation_chart=inflation_date['2014-06-04':].hvplot(kind='line',width=650,height=400,ylabel='Inflation indicator',xlabel='Date',title='Inflation Chart')

  st.write(hv.render(inflation_chart,backend='bokeh'))






