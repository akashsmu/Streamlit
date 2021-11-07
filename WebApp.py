import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from PIL import Image
import streamlit as st


st.title("""
Diabetes Detection
""")
st.subheader("""
Detect if someone has diabetes using Machine learning and python""")

image=Image.open("C:\\Users\\Akash smu\\Desktop\\ML.jpg")
st.image(image,use_column_width=True)

df=pd.read_csv('diabetes.csv')
st.subheader('Data Information:')
st.dataframe(df)
st.write(df.describe())
chart=st.bar_chart(df)

X=df.iloc[:,:8].values
Y=df.iloc[:,-1].values

X_train,X_test,Y_train,Y_test=train_test_split(
    X,Y,test_size=0.25,random_state=0
)

st.sidebar.header('User Input Parameters')

def get_user_input():
    Preg=st.sidebar.slider('Pregnancies',0,17,3)
    Glu=st.sidebar.slider('Glucose',0,199,117)
    BP=st.sidebar.slider('Blood Pressure',0,122,72)
    SkinT=st.sidebar.slider('Skin Thickness',0,99,50)
    Insulin=st.sidebar.slider('Insulin',0.0,846.0,30.5)
    BMI=st.sidebar.slider('BMI',0.0,67.1,32.0)
    DBF=st.sidebar.slider('DBF',0.078,2.42,0.3725)
    Age=st.sidebar.slider('Age',0,81,29)
    data={'Pregnancies':Preg, 'Glucose':Glu,'Blood_Pressure':BP,'Skin_Thickness':SkinT,
          'Insulin':Insulin,'BMI':BMI,'DBF':DBF,'Age':Age
          }
    data=pd.DataFrame(data,index=[0])
    return data

user_data=get_user_input()

rf=RandomForestClassifier()
rf.fit(X_train,Y_train)

st.subheader('Model Test Accuracy Score:')
st.write(str(accuracy_score(Y_test,rf.predict(X_test))*100)+'%')

st.subheader('User Input:')
st.write(user_data)


predict=rf.predict(user_data)
st.subheader('Classification:')
st.write(predict)

prediction=rf.predict_proba(user_data)
st.write(prediction)

