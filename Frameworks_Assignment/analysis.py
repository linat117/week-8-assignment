# import 
import pandas as pd 
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
#load the data 
df = pd.read_csv('metadata.csv')
# quick look at the data
print("Shape of data: ", df.shape)
print(df.info())
print(df.head())
print(df.isnull().sum())

#drop rows with out abstracts or publish time
df_clean = df.dropna(subset=['abstract', 'publish_time'])

#fill missing journal names

df_clean['journal'].fillna('Unknown', inplace=True)
# Convert publish_time to datetime
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

# Extract publication year
df_clean['year'] = df_clean['publish_time'].dt.year

# Optional: add abstract word count
df_clean['abstract_word_count'] = df_clean['abstract'].apply(lambda x: len(str(x).split()))

#Data analysis and visualization
year_counts = df_clean['year'].value_counts().sort_index()
plt.bar(year_counts.index, year_counts.values)
plt.xlabel('Year')
plt.ylabel('Number of Papers')
plt.title('Publications by Year')
plt.show()

#top journals
top_journals = df_clean['journal'].value_counts().head(10)
top_journals.plot(kind='bar')
plt.title('Top 10 Journals')
plt.xlabel('Journal')
plt.ylabel('Number of Papers')
plt.show()

# frequesnt words in titles

all_titles = ' '.join(df_clean['title'].dropna()).lower().split()
word_counts = Counter(all_titles)
print("Most common words in titles:", word_counts.most_common(20))

#wordcloud of titles


wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df_clean['title'].dropna()))
plt.figure(figsize=(15,7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

#distribution by ources
df_clean['source_x'].value_counts().plot(kind='bar')
plt.title('Distribution by Source')
plt.xlabel('Source')
plt.ylabel('Number of Papers')
plt.show()
