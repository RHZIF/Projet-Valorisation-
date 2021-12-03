import streamlit as st
import pandas as pd 
import json 
import requests
import codecs
import yfinance as yf
import base64
import investpy as py


st.title("Portfolio simulation dashboard")
tickers = {"atvi","adbe","amd","alxn","algn","goog","googl","amzn","amgn","adi","anss","aapl","amat","amat","asml","adsk","adp","bidu","biib","bmrn","bkng","avgo","cdns","cdw","cern","chtr","chkp","ctas","csco","ctxs","ctsh","cmcsa","cprt","cost","csx","dxcm","docu","dltr","ebay","ea","exc","expe","fb","fast","fisv","fox","foxa","gild","idxx","ilmn","incy","intc","intu","isrg","jd","klac","lrcx","lbtya","lbtyk","lulu","mar","mxim","meli","mchp","mu","msft","mrna","mdlz","mnst","ntes","nflx","nvda","nxpi","orly","pcar","payx","pypl","pep","pdd","qcom","regn","rost","sgen","siri","swks","splk","sbux","snps","tmus","ttwo","tsla","txn","khc","tcom","ulta","vrsn","vrsk","vrtx","wba","wdc","wday","xel","xlnx","zm"}
dropdown1 = st.selectbox('Pick your country', py.get_stock_countries())
dropdown = st.selectbox("Pick your assets", py.get_stocks(country=dropdown1).name)
start = st.date_input('Start', value = pd.to_datetime('2000-01-01'))
end = st.date_input('End', value = pd.to_datetime('today'))


df = yf.download(dropdown,
                      start, 
                      end, 
                      progress=False)




st.line_chart(df.Close)

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
