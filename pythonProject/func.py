import streamlit as st
import googleapiclient.discovery
import googleapiclient.errors
import re
import googleapiclient.discovery
import pandas as pd
from googletrans import Translator
import preprocess
import emoji
translator = Translator()
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

def translate_to_hindi(df , column_name):
    try:
        translator = Translator()
        df['Hindi_Text'] = df[column_name].apply(lambda text: translator.translate(text, src='en', dest='hi').text)
        return df
    except Exception as e:
        return None

def remove_emojis(text):
    emoji_pattern = re.compile("["
       u"\U0001F600-\U0001F64F"
       u"\U0001F300-\U0001F5FF"
       u"\U0001F680-\U0001F6FF"
       u"\U0001F700-\U0001F77F"
       u"\U0001F780-\U0001F7FF"
       u"\U0001F800-\U0001F8FF"
       u"\U0001F900-\U0001F9FF"
       u"\U0001FA00-\U0001FA6F"
       u"\U0001FA70-\U0001FAFF"
       u"\U0001FB00-\U0001FBFF"
       u"\U0001F004-\U0001F0CF"
       u"\U00002702-\U000027B0"
       u"\U000024C2-\U0001F251"
       "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def clean_text_column(df, column_name):
    html_pattern = re.compile(r'<.*?>')
    df[column_name] = df[column_name].apply(lambda x: re.sub(html_pattern, '', x))
    df[column_name] = df[column_name].apply(lambda x: re.sub(r'http\S+', '', x))
    df[column_name] = df[column_name].apply(lambda x: ' '.join(x.split()))
    df = df[~df[column_name].str.match(r'^[\W_]*$')]
    return df


def analyze_sentiment(text_column):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = text_column.apply(lambda x: analyzer.polarity_scores(x))
    sentiment_labels = sentiment_scores.apply(lambda x: get_sentiment_label(x))
    return sentiment_scores, sentiment_labels

def get_sentiment_label(sentiment_score):
    # Define sentiment thresholds
    threshold_positive = 0.05
    threshold_negative = -0.05
    threshold_informative = 0.1
    threshold_absurd = -0.1
    threshold_racist = -0.3

    # Assign sentiment labels based on thresholds
    if sentiment_score['compound'] >= threshold_positive:
        return 'positive'
    elif threshold_positive > sentiment_score['compound'] >= threshold_informative:
        return 'informative'
    elif threshold_informative > sentiment_score['compound'] >= threshold_absurd:
        return 'absurd'
    elif threshold_absurd > sentiment_score['compound'] >= threshold_racist:
        return 'racist'
    else:
        return 'non-racist'


def analyze_dataframe1(df):
    # Convert 'published_at' to datetime
    df['published_at'] = pd.to_datetime(df['published_at'])

    # Extract hour from 'published_at' and count comments per hour
    df['hour'] = df['published_at'].dt.hour
    hour_counts = df['hour'].value_counts().sort_index()

    # Plot comments per hour
    return hour_counts
    # plt.figure(figsize=(10, 5))
    # sns.barplot(x=hour_counts.index, y=hour_counts.values)
    # plt.title('Comments per Hour')
    # plt.xlabel('Hour')
    # plt.ylabel('Comment Count')
    # plt.show()

def analyze_dataframe2(df):
    words = ' '.join(df['English_noemoji_Text']).split()
    word_counts = pd.Series(words).value_counts().head(10)

    return word_counts

    # Plot the top 10 most common words
    # plt.figure(figsize=(10, 5))
    # sns.barplot(x=word_counts.index, y=word_counts.values)
    # plt.title('Top 10 Most Common Words')
    # plt.xlabel('Word')
    # plt.ylabel('Frequency')
    # plt.xticks(rotation=45)
    # plt.show()

def analyze_dataframe3(df):
    top_10_authors = df['author'].value_counts().head(10)

    return top_10_authors

def top_liked_comments(df):
    # Sort the DataFrame by 'like_count' in descending order
    sorted_df = df.sort_values(by='like_count', ascending=False)

    # Select the top 10 most liked comments
    top_10_comments = sorted_df.head(10)

    return top_10_comments


def analyze_sentiments(df):
    sentiment_counts = df['Sentiment_Labels_English_noemoji_Text'].value_counts()
    return sentiment_counts
    # Plot sentiment distribution
    # plt.figure(figsize=(6, 4))
    # sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
    # plt.title('Sentiment Distribution')
    # plt.xlabel('Sentiment')
    # plt.ylabel('Count')
    # plt.show()

def analyze_emojis(df):
    emoji_pattern = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U0001F004-\U0001F0CF\U0001F170-\U0001F251\U0001F004-\U0001F251]+", flags=re.UNICODE)
    
    # Extract emojis from the 'text' column
    emojis = [re.findall(emoji_pattern, text) for text in df['text']]
    emojis_flat = [emoji for sublist in emojis for emoji in sublist]
    
    emoji_counts = pd.Series(emojis_flat).value_counts()
    top_10_emojis = emoji_counts.head(10)

    return top_10_emojis

def analyze_comments_over_time(df):
    # Set the index to 'published_at'
    df.set_index('published_at', inplace=True)

    # Resample data on a daily basis
    daily_comments = df['like_count'].resample('D').count()
    daily_likes = df['like_count'].resample('D').sum()

    # Create a Streamlit app
    st.title("Comment Trends Over Time")
    st.dataframe(df, height=300)

    # Create a Matplotlib figure and axes
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the number of comments and likes over time
    ax.plot(daily_comments.index, daily_comments, label='Number of Comments', marker='o')
    ax.plot(daily_likes.index, daily_likes, label='Total Likes', marker='o')
    ax.set_title('Comment Trends Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Count')
    ax.legend()
    ax.grid(True)

    # Display the Matplotlib plot using st.pyplot
    st.pyplot(fig)

    return df

def analyze_and_display_largest_comments(df, N=5):
    # Calculate comment length
    df['comment_length'] = df['text'].apply(len)

    # Sort the DataFrame by comment length in descending order
    df = df.sort_values(by='comment_length', ascending=False)

    # Display the top N largest comments
    largest_comments = df.head(N)

    # Create a Streamlit app
    st.title(f"Top {N} Largest Comments")
    st.dataframe(largest_comments)

    return df