import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf

st.title('S&P 500 App')

st.markdown("""
This App retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python Libraries:** base64,streamlit,numpy,matplotlib,seaborn
* **Data Source:**[Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

st.sidebar.header('User Input Features')

@st.cache
def load_data():
    url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html=pd.read_html(url,header=0)
    df=html[0]
    return df

df=load_data()

sorted_sector_unique=sorted(df["GICS Sector"].unique())
sorted_sector=st.sidebar.multiselect('Sector',sorted_sector_unique,sorted_sector_unique)

df_selected_sector=df[df['GICS Sector'].isin(sorted_sector)]


st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

data=yf.download(
    tickers=list(df_selected_sector[:10].Symbol),
    period='ytd',
    interval='1d',
    group_by='ticker',
    auto_adjust=True,
    prepost=True,
    threads=True,
    proxy=None
)

def price_plot(symbol):
    df=pd.DataFrame(data[symbol].Close)
    df['Date']=df.index
    plt.fill_between(df.Date,df.Close,color='skyblue',alpha=0.3)
    plt.plot(df.Date,df.Close,color='skyblue',alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol,fontweight='bold')
    plt.xlabel('Date',fontweight='bold')
    plt.ylabel('Closing Price',fontweight='bold')
    return st.pyplot()

num_company=st.sidebar.slider("Number of companies",1,5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)






