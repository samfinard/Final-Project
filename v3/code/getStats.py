import pandas as pd
import ast

def addDateCount(filename):
    df = pd.read_csv(filename)
    df['dateRank'] = df['dateRank'].apply(ast.literal_eval)
    df['dateCount'] = df['dateRank'].apply(lambda x: len(x))
    df = df.sort_values(by='dateCount', ascending=False)
    df.to_csv("output.csv", index=False)

def main():
    # input = "/Users/samfinard/src/1PA/Final-Project/v3/data/lyricsToClean_2010-01-01_2021-11-06.csv"
    # addDateCount(input)
    df = pd.read_csv("/Users/samfinard/src/1PA/Final-Project/v3/output.csv")
    print(df['dateCount'].describe())
if __name__ == "__main__":
    main()

