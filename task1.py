import streamlit as st
import pandas as pd 
import json 
import requests
import codecs
import yfinance as yf
import base64
import investpy as py
from bs4 import BeautifulSoup
import re
import sys
import os
import http.cookiejar
import urllib.request, urllib.error, urllib.parse



def get_image(query):
    def get_soup(url,header):
        return BeautifulSoup(urllib.request.urlopen(
            urllib.request.Request(url,headers=header)),
            'html.parser')

    def bing_image_search(query):
        query= query.split()
        query='+'.join(query)
        url="http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

        #add the directory for your image here
        DIR="Pictures"
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = get_soup(url,header)
        image_result_raw = soup.find("a",{"class":"iusc"})

        m = json.loads(image_result_raw["m"])
        murl, turl = m["murl"],m["turl"]# mobile image, desktop image

        image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
        return (image_name,murl, turl)
    
    results = bing_image_search(query)
    return results[1]


st.title("Data scraper")


def stocks():
    dropdown1 = st.selectbox('Pick your country', py.get_stock_countries())
    dropdown = st.selectbox("Pick your assets", py.get_stocks(country=dropdown1).name)
    start = st.date_input('Start', value =pd.to_datetime('01-01-2000'))
    end = st.date_input('End', value = pd.to_datetime('today'))

    start = start.strftime('%d/%m/%Y')
    end = end.strftime('%d/%m/%Y')

    stocks = py.get_stocks(country=dropdown1)
    stocks.set_index("name", inplace = True)
    ticker =  stocks.loc[dropdown,'symbol']

    df=py.get_stock_historical_data(stock=ticker, country=dropdown1, from_date=start, to_date=end)

    url = get_image(str(dropdown))
    print(url)
    url = str(url)

    st.image(url, width=300)

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

def forex():
    dropdown = st.selectbox("Pick your pair", py.get_currency_crosses_list())
    start = st.date_input('Start', value =pd.to_datetime('01-01-2000'))
    end = st.date_input('End', value = pd.to_datetime('today'))

    start = start.strftime('%d/%m/%Y')
    end = end.strftime('%d/%m/%Y')

    df=py.get_currency_cross_historical_data(currency_cross=dropdown,from_date=start, to_date=end)

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

def crypto():
    dropdown = st.selectbox("Pick your asset", py.get_cryptos_list())
    start = st.date_input('Start', value =pd.to_datetime('01-01-2000'))
    end = st.date_input('End', value = pd.to_datetime('today'))

    start = start.strftime('%d/%m/%Y')
    end = end.strftime('%d/%m/%Y')

    df=py.get_crypto_historical_data(crypto=dropdown, from_date=start, to_date=end)

    url = get_image(str(dropdown))
    print(url)
    url = str(url)

    st.image(url, width=300)

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



# Create a page dropdown 
page = st.selectbox("Choose a market", ["Stocks", "Forex", "Crypto"]) 
if page == "Stocks":
    stocks()
elif page == "Forex":
    forex()
elif page == "Crypto":
    crypto()
