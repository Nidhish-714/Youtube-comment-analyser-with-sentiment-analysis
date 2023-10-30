import streamlit as st
import googleapiclient.discovery
import googleapiclient.errors
import re
import googleapiclient.discovery
import pandas as pd
from googletrans import Translator
import func
import preprocess
translator = Translator()
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.title("YouTube Comment Analysis")
# Input field for YouTube link
youtube_link = st.text_input("Enter the YouTube video URL:")

df = preprocess.prepro(youtube_link)
st.dataframe(df)

try:
    df = func.clean_text_column(df, 'text')
    # df = func.clean_text_column(df, 'Hindi_Text')
    # df = func.clean_text_column(df, 'Hindi_noemoji_Text')
    # df = func.clean_text_column(df, 'English_noemoji_Text')

except Exception as e:
        print(" ")


try:
    df['English_noemoji_Text'] = df['text'].apply(func.remove_emojis)
except Exception as e:
        print(" ")




try:
    sentiment_scores, sentiment_labels = func.analyze_sentiment(df['English_noemoji_Text'])
    df['Sentiment_Scores_English_noemoji_Text'] = sentiment_scores
    df['Sentiment_Labels_English_noemoji_Text'] = sentiment_labels
except Exception as e:
    print(" ")

try:
    df['published_at'] = pd.to_datetime(df['published_at'])
    df['date'] = df['published_at'].dt.date
    df['time'] = df['published_at'].dt.time
    df['month'] = df['published_at'].dt.month
except Exception as e:
    print(" ")






st.title('Translate Text to hindi')

st.subheader('Original Text (English):')
if st.button('Translate'):
    st.subheader('Translated Text (Hindi)     swipe left:')
    translated_df = func.translate_to_hindi(df, "text")
    if translated_df is not None:
                st.subheader('Translated DataFrame:')
                st.dataframe(translated_df)
                df = translated_df
    else:
                st.write('Translation Error')




try:
    df = func.clean_text_column(df, 'text')
    df = func.clean_text_column(df, 'Hindi_Text')
    df = func.clean_text_column(df, 'Hindi_noemoji_Text')
    df = func.clean_text_column(df, 'English_noemoji_Text')

except Exception as e:
        print(" ")




# try:
#     sentiment_scores, sentiment_labels = func.analyze_sentiment(df['English_noemoji_Text'])
#     df['Sentiment_Scores_English_noemoji_Text'] = sentiment_scores
#     df['Sentiment_Labels_English_noemoji_Text'] = sentiment_labels
# except Exception as e:
#     print(" ")

try:
    if(st.button('Analyze comments per hour')):
        func.analyze_dataframe1(df)
        st.pyplot()
except Exception as e:
    print(" ")

try:
    if(st.button('Analyze most common words')):
        func.analyze_dataframe2(df)
        st.pyplot()
except Exception as e:
    print(" ")

try:
    if(st.button('Top 10 authors with the most comments')):
        top_10_authors = func.analyze_dataframe3(df)
        st.subheader("Top 10 Authors with the Most Comments:")
        st.write(top_10_authors)
except Exception as e:
    print(" ")


try:
    if(st.button("Top 10 most liked comments")):
        temp_df = func.top_liked_comments(df)
        st.dataframe(temp_df)
except Exception as e:
    print(" ")

st.dataframe(df)







