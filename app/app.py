
# -------------
# Import libraries
# -------------

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

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

## Switch off warning
st.set_option('deprecation.showPyplotGlobalUse', False)


# -------------
# Import data
# -------------

df_twitter = pd.read_csv('streamlit_data.csv')

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

def create_gauge_pol(value,title="Polarity"):
    
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
                    {'range': [0.5, 1], 'color': 'green'}],
                'threshold': {
                    'line': {'color': "grey", 'width': 4},
                    'thickness': 0.75,
                    'value': value}}
            ),
        go.Layout(margin=go.layout.Margin(
                                l=0, #left margin
                                r=0, #right margin
                                b=0, #bottom margin
                                t=0, #top margin
                                )
            )
        )
    
    fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "white", 'family': "Arial"})
    return fig

def create_gauge_sub(value, title="Subjectivity"):
    fig = go.Figure(
        go.Indicator(
            mode = "gauge+number",
            value = value,
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
                    {'range': [0.75, 1], 'color': 'red'}],
                'threshold': {
                    'line': {'color': "grey", 'width': 4},
                    'thickness': 0.75,
                    'value': value}}),
            go.Layout(margin=go.layout.Margin(
                                    l=0, #left margin
                                    r=0, #right margin
                                    b=0, #bottom margin
                                    t=0, #top margin
                                    )
                )
            )
    
    fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "white", 'family': "Arial"})
    
    return fig

st.markdown("## Sentiment analysis")
sentiment = st.container()
with sentiment:
    #Create three columns/filters
    col1, col2 = st.columns(2)
    
    with col1:
        #st.markdown("### Polarity")
        
        polarity_value = 0.3
        st.plotly_chart(create_gauge_pol(polarity_value), use_container_width=True)
        
        st.markdown("### Polarity distribution")
        st.markdown("Some text")
        st.markdown("graph")

    with col2:
        #st.markdown("### Subjectivity")
        
        subjectivity_value = 0.1
        st.plotly_chart(create_gauge_sub(subjectivity_value), use_container_width=True)
        
        
        st.markdown("### Subjectivity distibution")
        st.markdown("Some text")
        st.markdown("graph")


# -------------- 
# Emotions
# -------------- 

clean_data_neutraless = df_twitter[df_twitter['emotion_label'] != 'neutral']
descending_order = clean_data_neutraless['emotion_label'].value_counts().sort_values(ascending=False).index[:10]
    

emotions = st.container()
with emotions: 
    st.markdown("## The top 10 Emotion")
    st.markdown("Description ...")
    
    fig = plt.figure(figsize=(10, 8))
    sns.countplot(data=clean_data_neutraless,y='emotion_label',order=descending_order)
    st.pyplot(fig)
       

emotion_cloud = st.container()
with emotion_cloud:
    #wordcloud plot
    st.markdown("## Emotion wordcloud")
    #drop down
    data_neutraless = df_twitter[df_twitter["sentiment_class"] != "neutral"] #droping the neutral class
    emotion = [st.selectbox( "Emotion", data_neutraless["sentiment_class"].unique())]  
    #filtered data
    df_emotion = data[data["sentiment_class"].isin(emotion)]
    
    all_words = ' '.join(twts for twts in df_emotion['cleaned_tweet'])

    text_cloud = WordCloud(height=300,width=500,random_state=10,max_font_size=110).generate(all_words)

    fig = plt.figure(figsize=(10,8))
    plt.imshow(text_cloud,interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)
           
# -------------- 
# Topic modeling
# -------------- 
        
st.markdown("## Currently treading topics")
topic_wcloud = st.container()
with topic_wcloud:
    #Create three columns/filters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("Select topic")
    with col2:
        st.markdown("word cloud")
        
st.markdown("## Popular words by topic")
topic_wcloud = st.container()
with topic_wcloud:
    #Create three columns/filters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Topic 1")
        st.markdown("Some text")
    with col2:
        st.markdown("### Topic 2")
        st.markdown("Some text")
          
st.markdown("## pyLDA visualisation")
pyLDA_vis = st.container()
with pyLDA_vis:
    st.markdown("big plot")              


# -------------- 
# Text generation
# -------------- 

st.markdown("## Text generation")
textgen = st.container()
with textgen:
    #Create three columns/filters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Enter key word(s)")
        st.markdown("box")
    with col2:
        st.markdown("### Selcect text length")
        st.markdown("slider")
    
    st.markdown("generated text")
