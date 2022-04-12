# -------------
# Import libraries
# -------------

import streamlit as st
from transformers import pipeline

## Switch off warnings
st.set_option('deprecation.showPyplotGlobalUse', False)

## Add side menu
## Add links to other pages/ features
st.sidebar.write("Additional Features:")
st.sidebar.write("[Home Page](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Home_Page/app.py)")
st.sidebar.write("[Sentiment Analysis](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Sentiment_Analysis/app.py)")
st.sidebar.write("[Emotions WordCloud](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Emotion_Cloud/app.py)")
st.sidebar.write("[Topic Model Visualization](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Topic_Modeling_Visualization/app.py)")
st.sidebar.write("[Topic WordCloud](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Topic_Cloud/app.py)")
 
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
  st.write("Select minimum character count on slider below.")
  article_min_word_count = st.slider('Article minimum character count', min_value=0, max_value=1000, value=200, step=50)
  

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

  



