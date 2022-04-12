# -------------
# Import libraries
# -------------

import streamlit as st
import pandas as pd
import numpy as np




import os
from wordcloud import wordcloud
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.decomposition import LatentDirichletAllocation


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

#df_twitter = df_twitter[df_twitter['date'].notnull()]

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

## Add side menu
## Add links to other pages/ features
st.sidebar.write("Additional Features:")
st.sidebar.write("[Home Page](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Home_Page/app.py)")
st.sidebar.write("[Sentiment Analysis](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Sentiment_Analysis/app.py)")
st.sidebar.write("[Emotions WordCloud](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Emotion_Cloud/app.py)")
st.sidebar.write("[Topic Model Visualization](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Topic_Modeling_Visualization/app.py)")
st.sidebar.write("[Text Generation](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Text_generation/app.py)")
 
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
dtm = cv.fit_transform(df_twitter['cleaned_tweet'].apply(lambda x: np.str_(x)))


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
    
    st.markdown("### Word Frequency by Topics")
  
    st.write("The lists below display the top 15 words for each topic modeled. The lists of words are utilized to label the discovered topics.")
  
  
    word_count = 15
  
    for i,topic in enumerate(LDA.components_):
      st.write("The top  {word_count} word for topic # {i} are:".format(word_count=word_count,i=i))
      st.write(" ")
      st.write(str([cv.get_feature_names()[index] for index in topic.argsort()[-word_count:]]))
      #st.write(print('\n'))
      #st.write(print('\n'))
    
    st.markdown("### Topic Word Cloud")
    st.write('Select topic from drop down menu below to visualize the most frequent words for the selected topic.')
    wordcloud_topic = st.radio("Topic for wordcloud",options=sorted(df_twitter['topic'].unique()))#,index=df_twitter['topic'].min()
    #st.selectbox
    
    topic_data = df_twitter[df_twitter['topic']==wordcloud_topic]
  
    topic_words = ' '.join(str(twts) for twts in topic_data['cleaned_tweet'])
  
    text_cloud = wordcloud.WordCloud(height=300,width=500,random_state=10,max_font_size=110).generate(topic_words)
  
    plt.figure(figsize=(10,8))
    plt.title('Topic Wordcloud')
    plt.imshow(text_cloud,interpolation='bilinear')
    plt.axis('off')
    #plt.show()
    st.pyplot()
