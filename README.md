# dsi-nlp-news
This repo is for hosting shared code and documents for the NLP project of DSI program 2022

## Introduction  
This repository details the work done by Scoop finders (Team C) for the [Africa Data Science Intensive (DSI) program](http://dsi-program.com/) Module 3 task. The goal of the task was to come up with an interesting natural language processing (NLP) project using either audio, text or both. 

We chose to create an app that provides an overview of one week of current twitter data. We chose to focus on tweets from Kenya, but this can easily be customised for another country or region. Our app is aimed at individuals working in the media industry who would like to supplement information gained from traditional media sources with information about currently treading topics on social media. In this way they would be able to better tailor their content to topics that are currently popular or trending. Our app also provides information on the sentiment and subjectively of the tweets as well as a text generation component that is intended to be used to provide background information or introduction. We have also allowed the user to adjust the date range so that they can analysis tweeter data, for example, on a specific date or over a weekend. 

## Streamlit app links

Bellow are the links to the different apps that make up the "Scoop finder" project. 

| App Description | Link |
|---|---|
| Home page | https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Home_Page/app.py |
| Sentiment Analysis |   https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Sentiment_Analysis/app.py |
| Emotion Cloud |   https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Emotion_Cloud/app.py |
| Topic modeling visualisation |   https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Topic_Modeling_Visualization/app.py |
| Topic cloud |    https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Topic_Cloud/app.py|
|  Text generation |  https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Text_generation/app.py |

The folder structure for the above repositories is:

- app.py : Main python script that powers streamlit application.
- requirements.txt : A text file with python libraries and dependencies.
- streamlit_data.csv : Twitter harvested dataset.
- Other support files e.g images and illustrations.

## Overview
Below we provide and overview of the different features of our app. 

### Sentiment analysis

### Emotion cloud

### Topic modeling visualisation
In this section of the app we find an overview of currently trending topics. The pyLADvis plot is in an interactive plot that allows the user to see and overview of the topics found using Latent Dirichlet Allocation (LDA). The user is also able to adjust the number of topics which is a hyperparameter of the LDA model.

### Topic cloud
In this section of the app we find details of the currently trending topics. Using LDA the top 15 words associated with each topic are determined and displayed. Below this the wordcloud of the selected topic is displayed.


### Text generation

In this section of the app we feed seed text to a transformer model GPT2 from the hugging face API. The seed text is based on discovered topics and themes from the twitter data.

## Report
I detailed report on there different aspects of this project can be found [here](https://github.com/tejlibre/dsi-nlp-news/blob/dev/Notebooks/Final%20Report.ipynb). Additonal supporting notebooks are also refered to in this report and can be found in the [notebooks folder](https://github.com/tejlibre/dsi-nlp-news/tree/dev/Notebooks). 

## Usage
