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

## drop missing data

df_twitter = pd.read_csv('streamlit_data.csv')

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
st.title("Our app name")

# # -------------- 
# # Word cloud
# # -------------- 



wcloud = st.container()
with wcloud:
  #Create two columns/filters
  #col1, col2 = st.columns(2)
    
  #with col1:
  st.subheader("What's Trending")
  st.markdown("The word cloud below displays words that appear most frequently in the trending tweets. The importance of words is shown with font size or color ")
  all_words = ' '.join(twts for twts in df_twitter['cleaned_tweet'])

  text_cloud = wordcloud.WordCloud(height=300,width=500,random_state=10,max_font_size=110).generate(all_words)

  plt.figure(figsize=(10,8))
  plt.title('All Tweets Wordcloud')
  plt.imshow(text_cloud,interpolation='bilinear')
  plt.axis('off')
  plt.show()
  st.pyplot()
    
    # with col2:
    #     st.subheader("Wordcloud Description.")
    #     st.markdown("This word cloud displays words that appear more frequently in the tweets. The importance of words is shown with font size or color ")

# -------------- 
# Senitiment analysis
# -------------- 

def create_gauge_pol(value,title="Average Polarity"):
    
    fig = go.Figure(
        go.Indicator(
            mode = "gauge+number",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title, 'font': {'size': 24}},
            gauge = {
                'axis': {'range': [-1,1], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [-1, -0.5], 'color': 'red'},
                    {'range': [-0.5, 0.5], 'color': 'orange'},
                    {'range': [0.5, 1], 'color': 'green'}],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': value}}
            ),
        go.Layout(margin=go.layout.Margin(
                                l=20, #left margin
                                r=20, #right margin
                                b=0, #bottom margin
                                t=0, #top margin
                                )
            )
        )
    
    fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "white", 'family': "Arial"})
    return fig

def create_gauge_sub(value, title="Average Subjectivity"):
    fig = go.Figure(
        go.Indicator(
            mode = "gauge+number",
            value = np.round(value*100)/100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title, 'font': {'size': 24}},
            gauge = {
                'axis': {'range': [0,1], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 0.25], 'color': 'green'},
                    {'range': [0.25, 0.75], 'color': 'orange'},
                    {'range': [0.75, 1], 'color': 'red'}],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': value}}),
            go.Layout(margin=go.layout.Margin(
                                    l=20, #left margin
                                    r=20, #right margin
                                    b=0, #bottom margin
                                    t=0, #top margin
                                    )
                )
            )
    
    fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "white", 'family': "Arial"})
    
    return fig

st.markdown("## Sentiment analysis")
st.markdown("The sentiment of a text can be either negative, neutral or positive. A measure of this is polarity. Polarity is a number between -1 and 1, where -1 corresponds to a highly negative sentiment, while +1 corresponds to a highly positive sentiment. ")
st.markdown("Subjectivity is judgment based on individual personal impressions and feelings and opinions rather than external facts. Here we also measure the subjectivity with 0 corresponding to highly factual statements, while highly emotional texts are scored with +1.")
sentiment = st.container()
with sentiment:
    #Create three columns/filters
    col1, col2 = st.columns(2)
    
    with col1:
        #st.markdown("### Polarity")
        
        polarity_value = df_twitter['polarity'].mean()
        st.plotly_chart(create_gauge_pol(polarity_value), use_container_width=True)
        
        

    with col2:
        #st.markdown("### Subjectivity")
        
        subjectivity_value =  df_twitter['subjectivity'].mean()
        st.plotly_chart(create_gauge_sub(subjectivity_value), use_container_width=True)
    
    st.markdown("### Polarity distribution")
    st.markdown("The figure below shows the distribution of tweets across the polarity spectrum. ")
    fig = ff.create_distplot([df_twitter['polarity'].to_list()],
                             ['Polarity'],
                             show_rug=False,
                             bin_size=.1
                             )
    
    fig.update(layout_showlegend=False)
    
    arrow_green = Image.open("arrow_green.png")
    fig.add_layout_image(
        dict(
            source=arrow_green,
            xref="x",
            yref="y",
            x=0.5,
            y=3,
            sizex=1,
            sizey=1.5,
            sizing="contain",
            opacity=0.5,
            layer="below")
    )

    arrow_red = Image.open("arrow_red.png")
    fig.add_layout_image(
        dict(
            source=arrow_red,
            xref="x",
            yref="y",
            x=-0.95,
            y=3,
            sizex=1,
            sizey=1.5,
            sizing="contain",
            opacity=0.5,
            layer="below")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    
    
    st.markdown("### Subjectivity distibution")
    st.markdown("The figure below shows the distribution of tweets across the subjectivity spectrum. ")
    fig = ff.create_distplot([df_twitter['subjectivity'].to_list()],
                             ['Subjectivity'],
                             show_rug=False,
                             bin_size=.05
                             )
    
    arrow_red = Image.open("arrow_red_flip.png")
    fig.add_layout_image(
        dict(
            source=arrow_red,
            xref="x",
            yref="y",
            x=0.65,
            y=6,
            sizex=3,
            sizey=3,
            sizing="contain",
            opacity=0.5,
            layer="below")
    )
    
    fig.update(layout_showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# -------------- 
# Emotions
# -------------- 


st.markdown("## Distribution of emotions")
emotions = st.container()
with emotions:
    #Create three columns/filters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("Graph")
    with col2:
        st.markdown("Some text")
        

st.markdown("## Positive and negative emotions")
emotions = st.container()
with emotions:
    #Create three columns/filters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("Some text")
    with col2:
        st.markdown("positive/negative buttons")
        st.markdown("word cloud")
        
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


## Attach topics to original dataset

topic_results = LDA.transform(dtm)

df_twitter['topic'] = topic_results.argmax(axis=1)


topic_wcloud = st.container()
with topic_wcloud:


  word_count = 15

  for i,topic in enumerate(LDA.components_):
    st.write("The top  {word_count} word for topic # {i} are:".format(word_count=word_count,i=i))
    st.write(str([cv.get_feature_names()[index] for index in topic.argsort()[-word_count:]]))
    #st.write(print('\n'))
    #st.write(print('\n'))

  wordcloud_topic = st.selectbox("Topic for wordcloud",options=df_twitter['topic'].unique(),index=df_twitter['topic'].min())

  topic_data = df_twitter[df_twitter['topic']==wordcloud_topic]

  topic_words = ' '.join(twts for twts in topic_data['cleaned_tweet'])

  text_cloud = wordcloud.WordCloud(height=300,width=500,random_state=10,max_font_size=110).generate(topic_words)

  plt.figure(figsize=(10,8))
  plt.title('Topic Wordcloud')
  plt.imshow(text_cloud,interpolation='bilinear')
  plt.axis('off')
  plt.show()
  st.pyplot()

         
st.markdown("## pyLDA visualisation")
pyLDA_vis = st.container()
with pyLDA_vis:
      
    html_string = pyLDAvis.prepared_data_to_html(pyLDAvis.sklearn.prepare(LDA, dtm, cv))

    components.v1.html(html_string, width=1300, height=800, scrolling=True)           


# -------------- 
# Text generation
# -------------- 

st.markdown("## Text generation")
textgen = st.container()
with textgen:

  ## Text box for user input (seed text)
  user_input = st.text_area("Input Seed Text")

  ## Slider to select number of words to be generated
  article_min_word_count = st.slider('Article minimum word count', min_value=0, max_value=1000, value=200, step=50)
  

  if st.button('Generate text'):

    ## Import generatot
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')

    ## Generate text
    text = generator(user_input, do_sample=True, min_length=article_min_word_count)

    ## Print text
    st.write(text[0]['generated_text'])