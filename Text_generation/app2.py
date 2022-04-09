# -------------
# Import libraries
# -------------

import streamlit as st
from streamlit import components
#import plotly.graph_objects as go
#import plotly.figure_factory as ff
import pandas as pd
#from PIL import Image




import numpy as np
import datetime as dt
import os
import re
import seaborn as sns
import datetime as dt
from wordcloud import wordcloud
import matplotlib.pyplot as plt

#from sklearn.feature_extraction.text import CountVectorizer
#import pyLDAvis
#import pyLDAvis.sklearn

#from transformers import pipeline


#from sklearn.decomposition import LatentDirichletAllocation

#from random import randint
#from pickle import load
#import random

# from keras.models import load_model
# from keras.preprocessing.sequence import pad_sequences
# from keras.preprocessing.text import Tokenizer

# import keras
# from keras.models import Sequential
# from keras.layers import Dense,LSTM,Embedding
# from tensorflow.keras.utils import to_categorical
# from pickle import dump,load

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

dates = st.sidebar.multiselect("Select dates of interest for wordcloud visualization",
options = df_twitter['date'].unique(),
default = df_twitter['date'].unique())

## Filter dataframe by selected dates

df_twitter = df_twitter[df_twitter["date"].isin(dates)]

## Add links to other pages/ features
st.sidebar.write("For further analysis select:")
st.sidebar.write("[Sentiment Analysis](https://share.streamlit.io/chrisliti/module3/main/app/app.py)")
st.sidebar.write("[Topic Modeling](https://share.streamlit.io/chrisliti/module3/main/app/app.py)")
st.sidebar.write("[Text Generation](https://share.streamlit.io/chrisliti/dsi-nlp-news/dev/Text_generation/app3.py)")

 
#Add title and subtitle to the main interface of the app
st.title('Scoop Finder')

# # -------------- 
# # Word cloud
# # -------------- 



wcloud = st.container()
with wcloud:

  
  st.subheader("What's Trending")
  st.markdown("The word cloud below displays words that appear most frequently in the trending tweets. The importance of words is shown with font size or color. ")
  all_words = ' '.join(twts for twts in df_twitter['cleaned_tweet'])

  text_cloud = wordcloud.WordCloud(height=300,width=500,random_state=10,max_font_size=110).generate(all_words)

  plt.figure(figsize=(10,8))
  plt.title('All Tweets Wordcloud')
  plt.imshow(text_cloud,interpolation='bilinear')
  plt.axis('off')
  plt.show()
  st.pyplot()

  st.markdown("""
  For more analysis select from the side bar options or click on the links below:
  - [Sentiment Analysis](https://share.streamlit.io/chrisliti/module3/main/app/app.py)
  - [Topic Modeling](https://share.streamlit.io/chrisliti/module3/main/app/app.py)
  - [Text Generation](https://share.streamlit.io/chrisliti/dsi-nlp-news/dev/Text_generation/app3.py)
  """)

    
  
