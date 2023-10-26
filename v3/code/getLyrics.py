import pandas as pd
import lyricsgenius
import ast
from tqdm import tqdm

genius = lyricsgenius.Genius("cm-U8F4lL_ZSZEu_wyPykBhTrWBFUwhFKZRwwhF9ZvKPK2BzoBdb2Ad1aQoazFy7g36x7vqltuzwsSeyVZ5vXQ")

def fetch_lyrics(song, artist):
    try:
        song_object = genius.search_song(song, artist)
        if song_object is not None:
            return song_object.lyrics
        else:
            return None
    except Exception as e:
        print(f"Missing lyrics for {song} by {artist}")
        return None

def filter_by_date(row, start_date, end_date):
    date_dict = ast.literal_eval(row['dateRank'])
    filtered_dict = {k: v for k, v in date_dict.items() if pd.Timestamp(k) >= pd.Timestamp(start_date) and pd.Timestamp(k) <= pd.Timestamp(end_date)}
    return str(filtered_dict) if filtered_dict else None

def getLyrics(start, end):
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    df = pd.read_csv("/Users/samfinard/src/1PA/Final-Project/v3/data/dateRank_1958_2021.csv")

    df['filtered_dateRank'] = df.apply(lambda row: filter_by_date(row, start, end), axis=1)
    df = df[df['filtered_dateRank'].notna()]
    df.drop('dateRank', axis=1, inplace=True)
    df.rename(columns={'filtered_dateRank': 'dateRank'}, inplace=True)
    
    
    df['lyrics'] = [fetch_lyrics(row['song'], row['artist']) for _, row in tqdm(df.iterrows(), total=df.shape[0])]
    
    df.to_csv(f'dateRankLyrics_{start.strftime("%Y-%m-%d")}_{end.strftime("%Y-%m-%d")}.csv', index=False)

def main():
    start, end = "01/01/2018", "10/26/2023"
    getLyrics(start, end)    
    
if __name__ == "__main__":
    main()
