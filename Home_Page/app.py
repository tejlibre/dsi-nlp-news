
# -------------
# Import libraries
# -------------

import streamlit as st
import pandas as pd
import os
from wordcloud import wordcloud
import matplotlib.pyplot as plt

## Switch off warnings
st.set_option('deprecation.showPyplotGlobalUse', False)

# -------------
# Import data
# -------------

## Load data
path = os.path.dirname(__file__)
df_twitter = pd.read_csv(path+'/streamlit_data.csv')

## Drop missing data

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
st.sidebar.write("Additional Features:")
st.sidebar.write("[Sentiment Analysis](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Sentiment_Analysis/app.py)")
st.sidebar.write("[Emotions WordCloud](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Emotion_Cloud/app.py)")
st.sidebar.write("[Topic Model Visualization](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Topic_Modeling_Visualization/app.py)")
st.sidebar.write("[Topic WordCloud](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Topic_Cloud/app.py)")
st.sidebar.write("[Text Generation](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Text_generation/app.py)")


#Add title and subtitle to the main interface of the app
st.title('Scoop Finder')

#  -------------- 
#  Word cloud
#  -------------- 

wcloud = st.container()
with wcloud:
    st.subheader("What's Trending")
    st.markdown("The word cloud below displays words that appear most frequently in the trending tweets. The importance of words is shown with font size or color. ")
    all_words = ' '.join(twts for twts in df_twitter['cleaned_tweet'])
    
    text_cloud = wordcloud.WordCloud(height=300,width=500,random_state=10,max_font_size=110).generate(all_words)
    
    # Show word cloud
    plt.figure(figsize=(10,8))
    plt.title('All Tweets Wordcloud')
    plt.imshow(text_cloud,interpolation='bilinear')
    plt.axis('off')
    plt.show()
    st.pyplot()

    st.markdown("""
    For more analysis select from the side bar options or click on the links below:
    - [Sentiment Analysis](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Sentiment_Analysis/app.py)
    - [Emotions Wordcloud](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Emotion_Cloud/app.py)
    - [Topic Model Visualization](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Topic_Modeling_Visualization/app.py)
    - [Topic WordCloud](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Topic_Cloud/app.py)
    - [Text Generation](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Text_generation/app.py)
    """)
