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

from transformers import pipeline


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


# # -------------
# # Import data
# # -------------

# #path = "C:/Users/Amy/Desktop/DSI/Module3/"
# #df_twitter = pd.read_csv(path+'streamlit_data.csv')


# path = os.path.dirname(__file__)
# df_twitter = pd.read_csv(path+'/streamlit_data.csv')

# ## drop missing data

# df_twitter = df_twitter[df_twitter['date'].notnull()]

# ## Convert date feature
# df_twitter['date'] = pd.to_datetime(df_twitter['date']).dt.date
# #Add sidebar to the app
# ## Create sidebar for filtering regions
# st.sidebar.header("Date Filter")

# dates = st.sidebar.multiselect("Select dates of interest for wordcloud visualization",
# options = df_twitter['date'].unique(),
# default = df_twitter['date'].unique())

# ## Filter dataframe by selected dates

# df_twitter = df_twitter[df_twitter["date"].isin(dates)]

# ## Add links to other pages/ features
# st.sidebar.write("For further analysis select:")
# st.sidebar.write("[Home Page](https://share.streamlit.io/chrisliti/module3/main/app/app.py)")
# st.sidebar.write("[Sentiment Analysis](https://share.streamlit.io/chrisliti/module3/main/app/app.py)")
# st.sidebar.write("[Topic Modeling](https://share.streamlit.io/chrisliti/module3/main/app/app.py)")


 
#Add title and subtitle to the main interface of the app
st.title('Scoop Finder')

# -------------- 
# Text generation
# -------------- 


st.markdown("## Text generation")
textgen = st.container()
with textgen:

  st.write("The section below uses transformers (deep learning models) to generate text for a specified topic of interest. Based on the discovered topics from the topic model, input seed text in the text box below to auto-generate an article.")

  ## Text box for user input (seed text)
  user_input = st.text_input("Type seed text to be fed to model below.","Input seed text")

  ## Slider to select number of words to be generated
  st.write("Select minimum word count on slider below.")
  article_min_word_count = st.slider('Article minimum word count', min_value=0, max_value=1000, value=200, step=50)
  

  if st.button('Generate text'):
    with st.spinner("Generating Text"):
      ## Import generatot
      generator = pipeline('text-generation', model='gpt2')

      ## Generate text
      text = generator(user_input, do_sample=True, min_length=article_min_word_count)

      ## Print text
      st.write(text[0]['generated_text'])
      
      ## Create file and dump generated text
      text_contents = text[0]['generated_text']
      st.download_button('Download Article', text_contents)

  
## Add links to other pages/ features
st.sidebar.write("For further analysis select:")
st.sidebar.write("[Home Page](https://share.streamlit.io/chrisliti/dsi-nlp-news/dev/Home_Page/app.py)")
st.sidebar.write("[Sentiment Analysis](https://share.streamlit.io/chrisliti/module3/main/app/app.py)")
st.sidebar.write("[Topic Modeling](https://share.streamlit.io/chrisliti/module3/main/app/app.py)")

