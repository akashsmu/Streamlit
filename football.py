import streamlit as st
import numpy as np
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns

st.title('NFL Football Stats Explorer')

st.markdown("""
This App performs simple webscrapping of NFL player stats data!
* **Python libraries:** base64,pandas,streamlit
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/)
***
""")

st.sidebar.header('User Input Features')
selected_year=st.sidebar.selectbox('Year',list(reversed(range(1990,2020))))

@st.cache
def load_data(year):
    url='https://www.pro-football-reference.com/years/'+str(year)+'/rushing.htm'
    html=pd.read_html(url,header=1)
    df=html[0]
    raw=df.drop(df[df.Age=='Age'].index) # here we are removing header rows which are repeated.
    raw=df.fillna(0)
    playerstats=raw.drop(['Rk'],axis=1)
    return playerstats

playerstats=load_data(selected_year)


sorted_unique_teams=sorted(playerstats.Tm.unique())
selected_team=st.sidebar.multiselect('Team',sorted_unique_teams,sorted_unique_teams)

unique_pos=['RB','QB','WR','FB','TE']
selected_pos=st.sidebar.multiselect('Position',unique_pos,unique_pos)

df_selected_team=playerstats[(playerstats.Tm.isin(selected_team))& (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of selected Team(s)')
st.write('Data Dimension:  '+str(df_selected_team.shape[0])+' rows and '+str(df_selected_team.shape[1])+' columns.')
st.dataframe(df_selected_team)

if st.button('Intercorrelation Heatmap'):
    st.header('InterCorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df=pd.read_csv('output.csv')

    corr=df.corr()
    mask=np.zeros_like(corr)
    mask[np.triu_indices_from(mask)]=True
    with sns.axes_style('white'):
        f,ax=plt.subplots(figsize=(7,5))
        ax=sns.heatmap(corr,mask=mask,vmax=1,square=True)
    st.pyplot()