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
    plt.figure(figsize=(10, 5))
    sns.barplot(x=hour_counts.index, y=hour_counts.values)
    plt.title('Comments per Hour')
    plt.xlabel('Hour')
    plt.ylabel('Comment Count')
    plt.show()

def analyze_dataframe2(df):
    words = ' '.join(df['English_noemoji_Text']).split()
    word_counts = pd.Series(words).value_counts().head(10)

    # Plot the top 10 most common words
    plt.figure(figsize=(10, 5))
    sns.barplot(x=word_counts.index, y=word_counts.values)
    plt.title('Top 10 Most Common Words')
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.show()

def analyze_dataframe3(df):
    top_10_authors = df['author'].value_counts().head(10)

    return top_10_authors

def top_liked_comments(df):
    # Sort the DataFrame by 'like_count' in descending order
    sorted_df = df.sort_values(by='like_count', ascending=False)

    # Select the top 10 most liked comments
    top_10_comments = sorted_df.head(10)

    return top_10_comments
