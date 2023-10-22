import datetime
import pandas as pd
import sys
import ast

def downloadKaggle():
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('dhruvildave/billboard-the-hot-100-songs', unzip=True)

def getDateRank(start, end):
    start, end = pd.to_datetime(start), pd.to_datetime(end)
    df = pd.read_csv("../data/charts.csv", parse_dates=['date'])
    df = df[(df['date'] >= start) & (df['date'] <= end)]
    df = df.iloc[:, :4]
    grouped = df.groupby(['song', 'artist'])
    
    rows_list = []
    
    for (song, artist), group in grouped:
        group = group.sort_values('date', ascending=False)
        group['date'] = group['date'].dt.strftime('%Y-%m-%d')
        date_rank_dict = group.set_index('date')['rank'].to_dict()
        
        most_recent_date = max(date for date in date_rank_dict.keys())
        
        new_row = {'song': song, 'artist': artist, 'dateRank': date_rank_dict, 'mostRecentDate': most_recent_date}
        rows_list.append(new_row)
    
    new_df = pd.DataFrame(rows_list)
    
    new_df = new_df.sort_values('mostRecentDate', ascending=False)
    
    new_df.drop(columns=['mostRecentDate'], inplace=True)
    
    new_df.to_csv("dateRank.csv", index=False)

def main():
    # downloadKaggle()
    start, end = "01/01/1950", "10/22/2023"
    getDateRank(start, end)

if __name__ == "__main__":
    main()