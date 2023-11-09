import ast
import pandas as pd
from collections import Counter
from tqdm.auto import tqdm
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
tqdm.pandas()
nltk.download('vader_lexicon')

tqdm.pandas()

def makeCounter(lyrics):
    words = str(lyrics).split()
    filtered_words = [word for word in words if len(word) > 1]
    word_count = Counter(filtered_words)
    return dict(word_count.most_common())

def count_sentiments(counter_dict, sa_tool, threshold=0.1):
    num_pos = 0
    num_neg = 0
    num_neu = 0
    
    if sa_tool == 'V':
        sid = SentimentIntensityAnalyzer()
        for word, freq in counter_dict.items():
            sentiment_scores = sid.polarity_scores(word)
            if sentiment_scores['compound'] >= threshold:
                num_pos += freq
            elif sentiment_scores['compound'] <= -threshold:
                num_neg += freq
            else:
                num_neu += freq
                
    elif sa_tool == 'T':
        for word, freq in counter_dict.items():
            analysis = TextBlob(word)
            if analysis.sentiment.polarity > threshold:
                num_pos += freq
            elif analysis.sentiment.polarity < -threshold:
                num_neg += freq
            else:
                num_neu += freq
    else:
        return "Invalid SA tool specified"
    return {'pos': round(num_pos,1), 'neg': round(num_neg,1), 'neu': round(num_neu,1)}

def getSentiment(df, sa_tool='B', threshold=0.1):
    df['counter'] = df['counter'].progress_apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    if sa_tool == 'B':
        sid = SentimentIntensityAnalyzer()
        df['vSentiment'] = df['counter'].progress_apply(lambda x: count_sentiments(x, 'V', threshold))
        df['tSentiment'] = df['counter'].progress_apply(lambda x: count_sentiments(x, 'T', threshold))

        df[['vPos', 'vNeg', 'vNeu']] = df['vSentiment'].apply(pd.Series)
        df[['tPos', 'tNeg', 'tNeu']] = df['tSentiment'].apply(pd.Series)

    else:  # If either VADER or TextBlob is to be used
        df['sentiment'] = df['counter'].progress_apply(lambda x: count_sentiments(x, sa_tool, threshold))

        # Separate columns for positive, negative, and neutral counts
        df[['pos', 'neg', 'neu']] = df['sentiment'].apply(pd.Series)

    return df

def main():
    input_path = "/Users/samfinard/src/1PA/Final-Project/v3/data/cleanedLyrics_withCounter.csv"
    df = pd.read_csv(input_path, low_memory=False)
    df = getSentiment(df, sa_tool = 'B')
    df.to_csv("sentimentByWord.csv", index=False)

if __name__ == "__main__":
    main()





