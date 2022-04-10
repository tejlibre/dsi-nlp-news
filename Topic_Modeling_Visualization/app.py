# -------------
# Import libraries
# -------------

import streamlit as st
from streamlit import components
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
from PIL import Image




import numpy as np
import datetime as dt
import os
import re
import seaborn as sns
import datetime as dt
from wordcloud import wordcloud
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
import pyLDAvis
import pyLDAvis.sklearn

from transformers import pipeline


from sklearn.decomposition import LatentDirichletAllocation

from random import randint
from pickle import load
import random

from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

import keras
from keras.models import Sequential
from keras.layers import Dense,LSTM,Embedding
from tensorflow.keras.utils import to_categorical
from pickle import dump,load

## Switch off warnings
st.set_option('deprecation.showPyplotGlobalUse', False)


# -------------
# Import data
# -------------

#path = "C:/Users/Amy/Desktop/DSI/Module3/"
#df_twitter = pd.read_csv(path+'streamlit_data.csv')


path = os.path.dirname(__file__)
df_twitter = pd.read_csv(path+'/streamlit_data.csv')

## drop missing data

df_twitter = df_twitter[df_twitter['date'].notnull()]

## Convert date feature
df_twitter['date'] = pd.to_datetime(df_twitter['date']).dt.date
#Add sidebar to the app
## Create sidebar for filtering regions
st.sidebar.header("Date Filter")

dates = st.sidebar.multiselect("Select dates of interest",
options = df_twitter['date'].unique(),
default = df_twitter['date'].unique())

## Filter dataframe by selected dates

df_twitter = df_twitter[df_twitter["date"].isin(dates)]
 
#Add title and subtitle to the main interface of the app
st.title("Scoop Finder")


# -------------- 
# Topic modeling
# -------------- 
        
st.markdown("## Currently treading topics")


number_of_topics = st.slider('Number of topics', min_value=1, max_value=5, value=3, step=1)
## create vocabulary

cv = CountVectorizer(max_df=0.9,min_df=5,stop_words='english')

## Create Document term matrix
dtm = cv.fit_transform(df_twitter['cleaned_tweet'])


## Initialize number of topics
rand_topics = number_of_topics

## Create model instance
LDA = LatentDirichletAllocation(n_components=rand_topics,random_state=42)

## Fit model instance
LDA.fit(dtm)

         
st.markdown("## Topic modeling visualization")
pyLDA_vis = st.container()
with pyLDA_vis:
    
    st.write("The interactive visualization below helps in interprating the topics discovered by the model fit on the trending tweets data. Click on a topic to visualize the topics word composition and distribution.")
      
    html_string = pyLDAvis.prepared_data_to_html(pyLDAvis.sklearn.prepare(LDA, dtm, cv))
    
    components.v1.html(html_string, width=1300, height=1000,  scrolling=True)           


