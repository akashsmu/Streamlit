import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import ti

st.set_page_config(layout='wide')

image=Image.open('C:\\Users\\Akash smu\\Desktop\\logo.jpg')
st.image(image,width=500)

st.title('Crypto Price App')
st.markdown("""
This App retrieves cryptocurrency prices fr the top 100 crypto from the **CoinMarketCap**

""")

expander_bar=st.beta_expander('About')
expander_bar.markdown("""
* **Python libraries:** pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
* **Data source:** [CoinMarketCap](http://coinmarketcap.com)

""")

col1=st.sidebar
col2,col3=st.beta_columns([2,1])

col1.header('Input Options')
currency_price_list=col1.selectbox('Select currency for price',('USD','BTC','ETH'))


@st.cache
def load_data():
    cmc=requests.get('https://coinmarketcap.com')
    soup=BeautifulSoup(cmc.content,'html.parser')

