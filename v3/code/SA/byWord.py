import pandas as pd
from collections import Counter
from tqdm.auto import tqdm
tqdm.pandas()


def count_words(lyrics):
    words = str(lyrics).split()
    filtered_words = [word for word in words if len(word) > 1]
    word_count = Counter(filtered_words)
    return dict(word_count.most_common())

def main():
    input_path = "/Users/samfinard/src/1PA/Final-Project/v3/data/cleanedLyrics_2010_2021.csv"
    df = pd.read_csv(input_path)

    df['counter'] = df['lyrics'].progress_apply(count_words)
    df.drop('lyrics', axis=1, inplace=True)
    
    df = df.dropna(axis=1, how='all')
    # df = df[df['counter'].apply(lambda x: len(x) > 1 and 'nan' not in x)]

    df.to_csv("output.csv", index=False)

if __name__ == "__main__":
    main()





