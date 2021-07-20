import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time

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
currency_price_unit=col1.selectbox('Select currency for price',('USD','BTC','ETH'))


@st.cache
def load_data():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

    # for i in listings:
    #     coins[str(i['id'])] = i['slug']

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    for i in listings:
      coin_name.append(i['slug'])
      coin_symbol.append(i['symbol'])
      price.append(i['quote'][currency_price_unit]['price'])
      percent_change_1h.append(i['quote'][currency_price_unit]['percentChange1h'])
      percent_change_24h.append(i['quote'][currency_price_unit]['percentChange24h'])
      percent_change_7d.append(i['quote'][currency_price_unit]['percentChange7d'])
      market_cap.append(i['quote'][currency_price_unit]['marketCap'])
      volume_24h.append(i['quote'][currency_price_unit]['volume24h'])

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'price', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'market_cap', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    return df

df=load_data()

sorted_coin=sorted(df['coin_symbol'])
selected_coin=col1.multiselect('Cryptocurrency',sorted_coin,sorted_coin)

df_selected_coin=df[df['coin_symbol'].isin(selected_coin)]
num_coin=col1.slider('Display Top N coins',1,100,100)
df_coins=df_selected_coin[:num_coin]

percent_timeframe=col1.selectbox('Percent Change in time Frame',['7d','24h','1h'])
percent_dict={'7d':'percent_change_7d','24h':'percent_change_24h','1h':'percent_change_1h'}
selected_timeframe=percent_dict[percent_timeframe]


col2.subheader('Price Data of selected CryptoCurrency')
col2.dataframe(df_coins)

# if st.button('View Data on selected timeframe'):
#     df_coin=df_coins[['coin_symbol','price',selected_timeframe]]
#     col2.dataframe(df_coin)

col2.subheader('Table of % Price Change')
df_change=pd.concat([df_coins.coin_symbol,df_coins.percent_change_1h,df_coins.percent_change_24h,df_coins.percent_change_7d],axis=1)
df_change=df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h']=df_change['percent_change_1h']>0
df_change['positive_percent_change_24h']=df_change['percent_change_24h']>0
df_change['positive_percent_change_7d']=df_change['percent_change_7d']>0

col2.dataframe(df_change)

col3.subheader('Bar Plot of % Price Change')

if percent_timeframe=='7d':
    col3.write('*7 days period')
    plt.figure(figsize=(5,15))
    plt.subplots_adjust(top=1,bottom=0)
    df_change['percent_change_7d'].plot(kind='barh',color=df_change.positive_percent_change_7d.map({True:'g',False:'r'}))
    col3.pyplot(plt)
elif percent_timeframe=='24h':
    col3.write('*24 hours period')
    plt.figure(figsize=(5,15))
    plt.subplots_adjust(top=1,bottom=0)
    df_change['percent_change_24h'].plot(kind='barh',color=df_change.positive_percent_change_24h.map({True:'g',False:'r'}))
    col3.pyplot(plt)
else:
    col3.write('*1 hour period')
    plt.figure(figsize=(5, 15))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_1h'].plot(kind='barh',
                                         color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
