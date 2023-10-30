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
        hour_counts = func.analyze_dataframe1(df)
        fig,ax = plt.subplots()
        sns.barplot(x=hour_counts.index, y=hour_counts.values, ax=ax)
        ax.set_title('Comments per Hour')
        ax.set_xlabel('Hour')
        ax.set_ylabel('Comment Count')
        st.pyplot(fig)
except Exception as e:
    print(" ")

try:
    if(st.button('Analyze most common words')):
        st.title("Top 10 Most Common Words Analysis")
        word_counts = func.analyze_dataframe2(df)
        st.dataframe(word_counts.reset_index().rename(columns={"index": "Word", 0: "Frequency"}), height=200)

        # Create a Matplotlib figure and axes
        fig, ax = plt.subplots(figsize=(10, 5))

        # Use Seaborn to create the barplot on the specified axes
        sns.barplot(x=word_counts.index, y=word_counts.values, ax=ax)

        # Set labels and title
        ax.set_title('Top 10 Most Common Words')
        ax.set_xlabel('Word')
        ax.set_ylabel('Frequency')

        # Rotate x-axis labels for better readability
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

        # Display the Matplotlib plot using st.pyplot
        st.pyplot(fig)
        
except Exception as e:
    print(" ")

try:
    if(st.button('Top 10 authors with the most comments')):
        st.title("Top 10 authors with the most comments")
        top_10_authors = func.analyze_dataframe3(df)
        st.subheader("Top 10 Authors with the Most Comments:")
        st.write(top_10_authors)
except Exception as e:
    print(" ")



try:
    if(st.button("Analyze emojis")):
        st.title("Top 10 Most Used Emojis Analysis")
        top_10_emojis = func.analyze_emojis(df)
        st.dataframe(top_10_emojis.reset_index().rename(columns={"index": "Emoji", 0: "Frequency"}), height=200)
        fig, ax = plt.subplots(figsize=(10, 5))

# Use Seaborn to create the barplot on the specified axes
        sns.barplot(x=top_10_emojis.index, y=top_10_emojis.values, ax=ax)

        # Set labels and title
        ax.set_title(' Most Used Emojis')
        ax.set_xlabel('Emoji')
        ax.set_ylabel('Frequency')

        # Rotate x-axis labels for better readability
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

        # Display the Matplotlib plot using st.pyplot
        st.pyplot(fig)

except Exception as e:
    print(" ")



try:
    if(st.button("Top 10 most liked comments")):
        st.write("Top 10 most liked comments")
        temp_df = func.top_liked_comments(df)
        st.dataframe(temp_df)
except Exception as e:
    print(" ")

try:
    if(st.button("Analyze Sentiments")):
        sentiment_counts = func.analyze_sentiments(df)
        st.title("Sentiment Distribution Analysis")
        st.dataframe(sentiment_counts.reset_index().rename(columns={"index": "Sentiment", "Sentiment_Labels_English_noemoji_Text": "Count"}), height=200)

        # Create a Matplotlib figure and axes
        fig, ax = plt.subplots(figsize=(6, 4))

        # Use Seaborn to create the barplot on the specified axes
        sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax)

        # Set labels and title
        ax.set_title('Sentiment Distribution')
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Count')

        # Display the Matplotlib plot using st.pyplot
        st.pyplot(fig)

except Exception as e:
    print(" ")


try:
    if(st.button("analyze comments over time")):
        df = func.analyze_comments_over_time(df)
except Exception as e:
     print(" ")


try:
    if(st.button("analyze longest comments")):
        N = 5  # Change N to the desired number of top largest comments
        df = func.analyze_and_display_largest_comments(df, N)
except Exception as e:
     print(" ")



st.write("Comments with all Sentiment Analysis")
st.dataframe(df)




