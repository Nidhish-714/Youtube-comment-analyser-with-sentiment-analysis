import streamlit as st
import googleapiclient.discovery
import googleapiclient.errors
import re
import googleapiclient.discovery
import pandas as pd
import pandas as pd
from googletrans import Translator


translator = Translator()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from textblob import TextBlob
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer




def extract_video_id(youtube_url):
    video_id_match = re.search(r'[?&]v=([a-zA-Z0-9_-]+)', youtube_url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        return None

def prepro(youtube_link):
    if youtube_link and extract_video_id(youtube_link):
        video_id = extract_video_id(youtube_link)

        # Initialize YouTube API
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyAjqoiVk-LQUFl-jjjfO87gfeuKFInUpFU"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)

        # Retrieve comments for the video
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        )
        response = request.execute()

        # Extract and store comments in a DataFrame
        comments = []

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay']
            ])

        df = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])

        return df
    else:

        st.warning("Please enter a valid YouTube video URL.")

