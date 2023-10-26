import pandas as pd
from langdetect import detect
from tqdm import tqdm
tqdm.pandas()

def isEnglish(text):
    return detect(text) == 'en'

inputFile = "/Users/samfinard/src/1PA/Final-Project/v3/data/dateRankLyrics_2018-01-01_2023-10-26.csv"
df = pd.read_csv(inputFile)

parts = inputFile.split('_')
start, end = parts[1], parts[2]

numMissing = df['lyrics'].isna().sum()
df.dropna(subset=['lyrics'], inplace=True)

df['isEn'] = df['lyrics'].progress_apply(isEnglish) # for visualization

numEng = df['isEn'].sum()
numNot = len(df) - numEng

df = df[df['isEn'] != 0]
df.drop('isEn', axis=1, inplace=True)

print(f"numMissing: {numMissing}")
print(f"numOtherLang: {numNot}")
print(f"numEng: {numEng}")


df.to_csv(f"lyricsToClean_{start}_{end}", index=False)