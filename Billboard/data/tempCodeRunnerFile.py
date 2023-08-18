merged_df = pd.merge(main, lyrics[['song', 'artist', 'lyrics']], on=['song', 'artist'], how='left')

merged_df.to_csv('merged.csv', index=False)