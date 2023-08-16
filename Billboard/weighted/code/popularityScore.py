import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm.notebook import tqdm
import time
import os

# Load the CSV file
file_path = '../data/popularity_score_minus_one.csv'
df = pd.read_csv(file_path)

# Spotify credentials
client_id = '3c8e482576ad422496c80f336bcf86eb'
client_secret = '3e84a42eca214b28adb96c2fae2d7bb9'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

count = 0
for i in tqdm(range(len(df)), desc="Fetching popularity"):
    try:
        artist = df.loc[i, 'artist']
        song = df.loc[i, 'song']
        results = sp.search(q='artist:' + artist + ' track:' + song, type='track')
        if results and results['tracks']['items']:
            df.loc[i, 'popularity'] = results['tracks']['items'][0]['popularity']
        else:
            df.loc[i, 'popularity'] = -1
            count += 1
    except Exception as e:
        print(f"An error occurred at index {i}: {str(e)}")
        df.loc[i, 'popularity'] = -1
        count += 1

    # Print progress every 100 songs
    if i % 100 == 0 and i != 0:
        print(f"Progress: {i} songs processed. {count} songs with no popularity score.")

# Saving the updated DataFrame
df.to_csv('updated_file.csv', index=False)