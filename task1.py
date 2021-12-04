import streamlit as st
import pandas as pd 
import json 
import requests
import codecs
import yfinance as yf
import base64
import investpy as py
import datetime


st.title("Stock data scraper")

dropdown1 = st.selectbox('Pick your country', py.get_stock_countries())
dropdown = st.selectbox("Pick your assets", py.get_stocks(country=dropdown1).name)
start = st.date_input('Start', value =pd.to_datetime('01-01-2000'))
end = st.date_input('End', value = pd.to_datetime('today'))

start = start.strftime('%d/%m/%Y')
end = end.strftime('%d/%m/%Y')

#df = py.get_stock_historical_data(stock=dropdown, country=dropdown1, from_date= start, to_date= end)
stocks = py.get_stocks(country=dropdown1)
stocks.set_index("name", inplace = True)
ticker =  stocks.loc[dropdown,'symbol']
#df = yf.download(ticker,start, end, progress=False)
df=py.get_stock_historical_data(stock=ticker, country=dropdown1, from_date=start, to_date=end)

st.line_chart(df.Close)
st.text('historique des cours de '+str(dropdown)+' : ')

st.dataframe(df)


def convert_df(tdf):
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name= str(dropdown) +'.csv',
     mime='text/csv',
 )
