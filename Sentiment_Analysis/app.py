# -------------
# Import libraries
# -------------

import streamlit as st
from streamlit import components
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px

import pandas as pd
from PIL import Image

import numpy as np
import datetime as dt
import os
import re
import datetime as dt
from wordcloud import wordcloud
import matplotlib.pyplot as plt

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
# Senitiment analysis
# -------------- 

def create_gauge_pol(value,title="Average Polarity"):
    fig = go.Figure(
        go.Indicator(
            mode = "gauge+number",
            value = value,
            number = {'valueformat':'.2f', 'font' : {'color' : 'blue'}},
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title, 'font': {'size': 24, 'color': 'blue'}},
            gauge = {
                'axis': {'range': [-1,1], 'tickwidth': 1, 'tickcolor': "lightblue"},
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
    

    fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "blue", 'family': "Arial"})
    return fig

def create_gauge_sub(value, title="Average Subjectivity"):
    fig = go.Figure(
        go.Indicator(
            mode = "gauge+number",
            value = value,
            number = {'valueformat':'.2f',  'font': {'color': 'blue'}},
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title, 'font': {'size': 24, 'color': 'blue'}},
            gauge = {
                'axis': {'range': [0,1], 'tickwidth': 1, 'tickcolor': "lightblue"},
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
    
    fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "blue", 'family': "Arial"})
    
    return fig

st.markdown("## Sentiment analysis")
with st.expander("See explanation"):
    st.markdown("The sentiment of a text can be either negative, neutral or positive. A measure of this is polarity. Polarity is a number between -1 and 1, where -1 corresponds to a highly negative sentiment, while +1 corresponds to a highly positive sentiment. ")
    st.markdown("Subjectivity is judgment based on individual personal impressions and feelings and opinions rather than external facts. Here we also measure the subjectivity with 0 corresponding to highly factual statements, while highly emotional texts are scored with +1.")
sentiment = st.container()
with sentiment:
    #Create three columns/filters
    col1, col2 = st.columns(2)
    
    with col1:
        #st.markdown("### Polarity")
        
        polarity_value = df_twitter['polarity'].mean()
        
        if polarity_value >= 0:
            if polarity_value > 0.5:
                st.markdown('### Strong positive sentiment')
                st.markdown('On average tweets reflect an enthusiastic, happy or excited mood.')
            else:
                st.markdown('### Weak positive sentiment')
                st.markdown('On average tweets reflect a slightly enthusiastic, happy or excited mood.')
        else:
            if polarity_value < 0:
                if polarity_value < -0.5:
                    st.markdown('### Strong negative sentiment')
                    st.markdown('On average tweets reflect a pessimistic, unfavorable or uphappy mood.')
                else:
                    st.markdown('### Weak negative sentiment')
                    st.markdown('On average tweets reflect a slightly pessimistic, unfavorable or uphappy mood.')


    with col2:
        #st.markdown("### Subjectivity")
        
        subjectivity_value =  df_twitter['subjectivity'].mean()
        
        if subjectivity_value >= 0.25:
            if polarity_value > 0.75:
                st.markdown('### Strongly subjective')
                st.markdown('On average tweets are very subjective.')
            else:
                st.markdown('### Weakly subjective')
                st.markdown('On average tweets are somewhat subjetive.')
        else:
            if subjectivity_value < 0.5:
                if polarity_value < 0.25:
                    st.markdown('### Factual')
                    st.markdown('On average tweets are strongly factual.')
                else:
                    st.markdown('### Somewhat factual')
                    st.markdown('On average tweets are factual but include some subjectivity.')
         
        
    col1, col2 = st.columns(2)
    with col1:   
        st.plotly_chart(create_gauge_pol(polarity_value), use_container_width=True)
        
    with col2:           
        st.plotly_chart(create_gauge_sub(subjectivity_value), use_container_width=True)
    
      
st.markdown("### Polarity distribution")
st.markdown("The figure below shows the distribution of tweets across the polarity spectrum. ")
with st.expander("See explanation"):
    st.markdown("Polarity is a number between -1 and 1. A sentiment becomes more negative as the polarity moves from 0 to -1 with -1 corresponding to a highly negative sentiment. The sentiment decomes more positive as the polarity moves from 0 towords +1 with +1 corresponding to a highly positive sentiment. ")
    
polarity = st.container()
with polarity:
    fig = ff.create_distplot([df_twitter['polarity'].to_list()],
                             ['Polarity'],
                             show_rug=False,
                             bin_size=.1
                             )
    
    fig.update(layout_showlegend=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(
    xaxis_title="Polarity",
    yaxis_title="Frequecy")
    
    arrow_green = Image.open(path+"/arrow_green.png")
    fig.add_layout_image(
        dict(
            source=arrow_green,
            xref="x",
            yref="y",
            x=0.35,
            y=3,
            sizex=1,
            sizey=1.5,
            sizing="contain",
            opacity=0.5,
            layer="below")
    )

    arrow_red = Image.open(path+"/arrow_red.png")
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
with st.expander("See explanation"):
    st.markdown("With the subjectivity measure, 0 corresponds to highly factual statements i.e a sentiment is more objective, while highly emotional texts are scored with +1 which means the sentiment is more subjective based on the individual emotions.")
    
subjectivity = st.container()
with subjectivity:
    fig = ff.create_distplot([df_twitter['subjectivity'].to_list()],
                             ['Subjectivity'],
                             show_rug=False,
                             bin_size=.05
                             )
    
    arrow_red = Image.open(path+"/arrow_red_flip.png")
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
    
    arrow_green = Image.open(path+"/arrow_green_flip.png")
    fig.add_layout_image(
        dict(
            source=arrow_green,
            xref="x",
            yref="y",
            x=0.1,
            y=6,
            sizex=3,
            sizey=3,
            sizing="contain",
            opacity=0.5,
            layer="below")
    )
    
    fig.update_layout(
    xaxis_title="Subjectivity",
    yaxis_title="Frequecy")
    fig.update(layout_showlegend=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True)

# -------------- 
# Emotions
# -------------- 


clean_data_neutraless = df_twitter[df_twitter['emotion_label'] != 'neutral']
df_emotion = clean_data_neutraless['emotion_label'].value_counts().sort_values()
df_emotion = pd.DataFrame(df_emotion,columns=['emotion_label','count'])
df_emotion.reset_index(inplace=True)

df_descriptions = pd.read_csv(path+'/emotions.txt', sep=';')
df_new = pd.merge(df_emotion, df_descriptions, on ='index', how ="outer")

emotions = st.container()
with emotions: 
    st.markdown("## The top 10 Emotion")
    st.markdown("This bar graph shows the top 10 most common emotions detected in the tweets from the chosen date range.")
    
    #fig = plt.figure(figsize=(10, 8))
    #sns.countplot(data=clean_data_neutraless,y='emotion_label',order=descending_order)
    #st.pyplot(fig)
    
    fig = px.bar(df_new.iloc[0:10], y='index', x='emotion_label',
             hover_data=['description'], color='emotion_label',
             orientation='h',
             labels={'emotion_label':'Count','index':'Emotions','description':'Description'}, height=400)
    fig.update(layout_coloraxis_showscale=False)
    fig.update_xaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True)
