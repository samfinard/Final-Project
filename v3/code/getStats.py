import pandas as pd
import ast

def safe_literal_eval(s):
    try:
        return ast.literal_eval(s)
    except ValueError:
        return []

def addDateCount(filename):
    df = pd.read_csv(filename, low_memory=False)
    df['dateRank'] = df['dateRank'].apply(lambda x: safe_literal_eval(x) if pd.notna(x) and isinstance(x, str) else [])
    df['dateCount'] = df['dateRank'].apply(len)
    df = df.sort_values(by='dateCount', ascending=False)
    df.to_csv("output.csv", index=False)


def dropMissingLyrics(filename):
    df = pd.read_csv(filename)
    orig_count = len(df)
    cleaned_df = df.dropna(subset=['lyrics'])
    dropped_count = orig_count - len(cleaned_df)
    print(f"{dropped_count} many missing lyrics.")
    cleaned_df.to_csv("droppedLyrics.csv")

def main():
    input = "/Users/samfinard/src/1PA/Final-Project/v3/data/cleanedLyrics_withCounter.csv"
    
    df = pd.read_csv(input, low_memory=False)
    

if __name__ == "__main__":
    main()

