import pandas as pd

existingLyrics = pd.read_csv("existingLyrics.csv")

print(existingLyrics['lyrics'].isna().sum())
