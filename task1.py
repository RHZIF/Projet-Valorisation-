import streamlit as st
import pandas as pd 
import requests
import investpy as py
from bs4 import BeautifulSoup
import plotly.express as px
import Casabourselib as cbl 

def ticker_2_CodeValeur(ticker):
  ticker_2_CodeValeur = {"ADH" : "9000" , "AFM" : "12200" , "AFI" : "11700" , "GAZ" : "7100" , "AGM" : "6700" , "ADI" : "11200" , "ALM" : "6600" , "ARD" : "27" , "ATL" : "10300" , "ATW" : "8200" , "ATH" : "3200" , "NEJ" : "7000" , "BAL" : "3300" , "BOA" : "1100" , "BCP" : "8000" , "BCI" : "5100" , "CRS" : "8900" , "CDM" : "3600" , "CDA" : "3900" , "CIH" : "3100" , "CMA" : "4000" , "CMT" : "11000" , "COL" : "9200" , "CSR" : "4100" , "CTM" : "2200" , "DRI" : "8500" , "DLM" : "10800" , "DHO" : "10900" , "DIS" : "4200" , "DWY" : "9700" , "NKL" : "11300" , "EQD" : "2300" , "FBR" : "9300" , "HPS" : "9600" , "IBC" : "7600" , "IMO" : "12" , "INV" : "9500" , "JET" : "11600" , "LBV" : "11100" , "LHM" : "3800" , "LES" : "4800" , "LYD" : "8600" , "M2M" : "10000" , "MOX" : "7200" , "MAB" : "1600" , "MNG" : "7300" , "MLE" : "2500" , "IAM" : "8001" , "MDP" : "6500" , "MIC" : "10600" , "MUT" : "21" , "NEX" : "7400" , "OUL" : "5200" , "PRO" : "9900" , "REB" : "5300" , "RDS" : "12000" , "RISMA" : "8700" , "S2M" : "11800" , "SAH" : "11400" , "SLF" : "10700" , "SAM" : "6800" , "SMI" : "1500" , "SNA" : "10500" , "SNP" : "9400" , "MSA" : "12300" , "SID" : "1300" , "SOT" : "9800" , "SRM" : "2000" , "SBM" : "10400" , "STR" : "11500" , "TQM" : "11900" , "TIM" : "10100" , "TMA" : "12100" , "UMR" : "7500" , "WAA" : "6400" , "ZDJ" : "5800"}
  return ticker_2_CodeValeur[ticker]


def get_image(ticker):                                                           
  url = "https://www.casablanca-bourse.com/bourseweb/Societe-Cote.aspx?codeValeur="+str(ticker_2_CodeValeur(ticker))+"&cat=7"
  req = requests.get(url)
  soup = BeautifulSoup(req.text, "html.parser")
  logo_path = soup.find("input", {"id": "SocieteCotee1_imgLogo"})['src']
  logo_url = 'https://www.casablanca-bourse.com/bourseweb/' + logo_path
  return logo_url

apptitle = 'Projet valorisation'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

# Title the app
st.title('Gravitational Wave Quickview')

st.markdown("""
 * Use the menu at left to select data and set plot parameters
 * Your plots will appear below
""")

@st.cache(ttl=3600, max_entries=10)   #-- Magic command to cache data

@st.cache(ttl=3600, max_entries=10)   #-- Magic command to cache data
    
# st.sidebar.markdown("## Selectioner le titre et la periode ")



st.markdown('## Realisé par: Yassine Rhzif, Ahmed Ouaboune, Mouad Rhafir, Anware Adnane')

col1,col3, col2 = st.columns(3)


select_event = .selectbox('How do you want to find data?',
                                    ['By event name', 'By GPS'])

dropdown = st.sidebar.selectbox("Choisir une action", py.get_stocks(country='morocco').name)
ma = st.sidebar.selectbox("Periode de calcule de la moyenne mobile (en jours)", [15,30,45,60])



start = st.sidebar.date_input('Debut', value =pd.to_datetime('01-01-2020'))
end = st.sidebar.date_input('Fin', value = pd.to_datetime('today'))

start = start.strftime('%d/%m/%Y')
end = end.strftime('%d/%m/%Y')

stocks = py.get_stocks(country='morocco')
stocks.set_index("name", inplace = True)
ticker =  stocks.loc[dropdown,'symbol']

df=py.get_stock_historical_data(stock=ticker, country='morocco', from_date=start, to_date=end)
df['Moving Average'] = df.Close.rolling(int(ma)).mean()

url = get_image(ticker)
print(url)
url = str(url)

col1.markdown('<center><img src="'+url+'" alt="stock logo"></center>', unsafe_allow_html=True)
indicators = cbl.get_indicators(ticker)
col1.dataframe(indicators)

data = [df['Close'], df['Moving Average']]
headers = ["Close", "Moving Average"]
df3 = pd.concat(data, axis=1, keys=headers)


fig = px.line(df3)

col1.plotly_chart(fig, use_container_width=False, sharing="streamlit")



