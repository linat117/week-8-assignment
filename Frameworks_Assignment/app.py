# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

# Load cleaned data
df = pd.read_csv('metadata.csv')
df = df.dropna(subset=['abstract','publish_time'])
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research papers interactively")

# Slider for year selection
year_range = st.slider("Select year range", 2019, 2022, (2020, 2021))
filtered_data = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.write(f"Showing {filtered_data.shape[0]} papers between {year_range[0]} and {year_range[1]}")

# Publications by year
fig, ax = plt.subplots()
year_counts_filtered = filtered_data['year'].value_counts().sort_index()
ax.bar(year_counts_filtered.index, year_counts_filtered.values)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Papers')
ax.set_title('Publications by Year')
st.pyplot(fig)

# Top journals
top_journals = filtered_data['journal'].value_counts().head(10)
st.bar_chart(top_journals)

# Word cloud
st.write("Word Cloud of Paper Titles")
all_titles = ' '.join(filtered_data['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
fig_wc, ax_wc = plt.subplots(figsize=(15,7))
ax_wc.imshow(wordcloud, interpolation='bilinear')
ax_wc.axis('off')
st.pyplot(fig_wc)

# Sample data
st.write("Sample Papers")
st.dataframe(filtered_data[['title','journal','year','source_x']].head(10))
