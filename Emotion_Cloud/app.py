# -------------
# Import libraries
# -------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from wordcloud import wordcloud

## Switch off warnings
st.set_option('deprecation.showPyplotGlobalUse', False)

# -------------
# Import data
# -------------

## Read twitter data
path = os.path.dirname(__file__)
df_twitter = pd.read_csv(path+'/streamlit_data.csv')

## Drop missing data
df_twitter = df_twitter[df_twitter['date'].notnull()]

## Convert date feature
df_twitter['date'] = pd.to_datetime(df_twitter['date']).dt.date

## Add sidebar to the app
## Create sidebar for filtering regions
st.sidebar.header("Date Filter")

dates = st.sidebar.multiselect("Select dates of interest",
options = df_twitter['date'].unique(),
default = df_twitter['date'].unique())

## Filter dataframe by selected dates
df_twitter = df_twitter[df_twitter["date"].isin(dates)]

## Add side menu
## Add links to other pages/ features
st.sidebar.write("Additional Features:")
st.sidebar.write("[Home Page](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Home_Page/app.py)")
st.sidebar.write("[Sentiment Analysis](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Sentiment_Analysis/app.py)")
st.sidebar.write("[Topic Model Visualization](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Topic_Modeling_Visualization/app.py)")
st.sidebar.write("[Topic WordCloud](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Topic_Cloud/app.py)")
st.sidebar.write("[Text Generation](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Text_generation/app.py)")
 
## Add title and subtitle to the main interface of the app
st.title("Scoop Finder")

clean_data_neutraless = df_twitter[df_twitter['emotion_label'] != 'neutral']
descending_order = clean_data_neutraless['emotion_label'].value_counts().sort_values(ascending=False).index[:10]
    
# -------------
# Wordcloud
# -------------

## Steamlit container
emotion_cloud = st.container()
with emotion_cloud:
    
    ## Wordcloud plot
    st.markdown("## Emotion wordcloud")
    st.markdown("Wordcloud showing words associated with either positive or negative emotions. The relative importance of words is shown with font size or color.")
    
    ## Drop down
    data_neutraless = df_twitter[df_twitter["sentiment_class"] != "neutral"] #droping the neutral class
    emotion = [st.selectbox( "Select from either positive or neagtive emotions:", data_neutraless["sentiment_class"].unique())]  
    
    ## Filtered data
    df_emotion = data_neutraless[data_neutraless["sentiment_class"].isin(emotion)]
    
    all_words = ' '.join(twts for twts in df_emotion['cleaned_tweet'])

    text_cloud = wordcloud.WordCloud(height=300,width=500,random_state=10,max_font_size=110).generate(all_words)

    ## Show wordcloud
    fig = plt.figure(figsize=(10,8))
    plt.imshow(text_cloud,interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)
        
