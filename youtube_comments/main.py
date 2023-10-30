import streamlit as st

# Set the page title
st.set_page_config(page_title="YOUTUBE COMMENT ANALYSIS")

# Streamlit app title
st.title("YouTube Comment Analysis")

# Input field for YouTube link
youtube_link = st.text_input("Enter the YouTube video URL:")

# Button to start analysis
if st.button("Start Analysis"):
    if not youtube_link:
        st.warning("Please enter a valid YouTube link.")
    else:
        # Perform your YouTube comment analysis here
        st.info(f"Analyzing comments for YouTube video: {youtube_link}")
        # Add your analysis code here
        # You can display the results using st.write, st.dataframe, or st.pyplot

# You can add more Streamlit components for visualizing the analysis results
