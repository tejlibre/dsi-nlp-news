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

## Add side menu
## Add links to other pages/ features
st.sidebar.write("Additional Features:")
st.sidebar.write("[Home Page](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Home_Page/app.py)")
st.sidebar.write("[Sentiment Analysis](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Sentiment_Analysis/app.py)")
st.sidebar.write("[Emotions WordCloud](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Emotion_Cloud/app.py)")
st.sidebar.write("[Topic WordCloud](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Topic_Cloud/app.py)")
st.sidebar.write("[Text Generation](https://share.streamlit.io/tejlibre/dsi-nlp-news/dev/Text_generation/app.py)")
 
#Add title and subtitle to the main interface of the app
st.title("Scoop Finder")


# -------------- 
# Topic modeling
# -------------- 
        
st.markdown("## Currently treading topics")

st.write('Select number of topics to be extracted from tweet data on the slider below.')
number_of_topics = st.slider('Number of topics', min_value=1, max_value=5, value=3, step=1)
st.write('Click on the Fit Model button below to fit a LDA model to the tweets data and visualize the topics.')


if st.button('Fit Model'):
 
  with st.spinner("Fitting Model"):
    
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

            
    st.markdown("## Topic modeling visualization")
    pyLDA_vis = st.container()
    with pyLDA_vis:
        
        st.write("The interactive visualization below helps in interprating the topics discovered by the model fit on the trending tweets data. Click on a topic to visualize the topics word composition and distribution.")
          
        html_string = pyLDAvis.prepared_data_to_html(pyLDAvis.sklearn.prepare(LDA, dtm, cv))
        
        components.v1.html(html_string, width=1300, height=1000,  scrolling=True)      
        

