import pandas as pd
import lyricsgenius
import time
from tqdm import tqdm

# Initialize the Genius API client
genius = lyricsgenius.Genius()

# Load the data
df = pd.read_csv('russian_songs.csv')

# Define a function to fetch lyrics
def fetch_lyrics(song, artist):
    try:
        song_object = genius.search_song(song, artist)
        if song_object is not None:
            return song_object.lyrics
        else:
            return None
    except Exception as e:
        print(f"Error occurred while fetching lyrics for song {song} by {artist}: {e}")
        return None

# Fetch lyrics for each song and add a 6-second delay between each call
df['lyrics'] = [fetch_lyrics(row['song'], row['artist']) for _, row in tqdm(df.iterrows(), total=df.shape[0])]
time.sleep(6)

# Save the modified DataFrame to a new CSV file
df.to_csv('russian_songs_with_lyrics.csv', index=False)
