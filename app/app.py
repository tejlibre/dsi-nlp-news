import streamlit as st
import pandas as pd

import plotly.graph_objects as go
import plotly.figure_factory as ff

# -------------
# Import data
# -------------

path = 'C:/Users/Amy/Desktop/DSI/Module3/'
df_twitter = pd.read_csv(path+'streamlit_data.csv')
print(df_twitter.info())

#Add sidebar to the app
st.sidebar.markdown("### Select stuff")
st.sidebar.markdown("blah blah")

#Add title and subtitle to the main interface of the app
st.title("Our app name")

# -------------- 
# Word cloud
# -------------- 

wcloud = st.container()
with wcloud:
    #Create three columns/filters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**word cloud**")
    
    with col2:
        st.markdown("## Word Cloud")
        st.markdown("Trendng topics on Twitter")

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
        
        polarity_value = df_twitter['polarity'].mean()
        st.plotly_chart(create_gauge_pol(polarity_value), use_container_width=True)
        
        

    with col2:
        #st.markdown("### Subjectivity")
        
        subjectivity_value =  df_twitter['subjectivity'].mean()
        st.plotly_chart(create_gauge_sub(subjectivity_value), use_container_width=True)
    
    st.markdown("### Polarity distribution")
    st.markdown("Some text")
    fig = ff.create_distplot([df_twitter['polarity'].to_list()],
                             ['Polarity'],
                             show_rug=False,
                             bin_size=.1
                             )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Subjectivity distibution")
    st.markdown("Some text")
    fig = ff.create_distplot([df_twitter['subjectivity'].to_list()],
                             ['Subjectivity'],
                             show_rug=False,
                             bin_size=.05
                             )
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