import pandas as pd

df = pd.read_csv('main.csv')

df = df[['song', 'artist', 'lyrics', 'track_popularity']]

print(len(df) - df['lyrics'].isnull().sum())