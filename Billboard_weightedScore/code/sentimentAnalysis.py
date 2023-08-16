import pandas as pd

from tqdm.notebook import tqdm
from tqdm import tqdm
tqdm.pandas()

import os

from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import tensorflow as tf
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

from flair.models import TextClassifier
from flair.data import Sentence


def addVader(inputFilePath):
    df = pd.read_csv(inputFilePath)
    sia = SentimentIntensityAnalyzer()
    df['vader'] = df.progress_apply(lambda row: sia.polarity_scores(str(row['lyrics']))['compound'], axis=1)
    df.to_csv(f"withVader.csv", index=False)

def addTextBlob(inputFilePath):
    df = pd.read_csv(inputFilePath)
    df['textblob'] = df.progress_apply(lambda row: TextBlob(str(row['lyrics'])).sentiment.polarity, axis=1)
    df.to_csv("withTextBlob.csv", index=False)

def addBertCheckpoint(inputFilePath, outputFile="withBert.csv", checkpointFile="bert_checkpoint.txt", batchSize=100):
    # Initialize the checkpoint
    if os.path.exists(checkpointFile):
        with open(checkpointFile, 'r') as f:
            checkpoint = f.read()
            startRow = int(checkpoint or 0)
    else:
        startRow = 0

    df = pd.read_csv(inputFilePath)

    # If output file exists, read it and get the 'bert' column. Otherwise, initialize 'bert' column with None.
    if os.path.exists(outputFile):
        df_out = pd.read_csv(outputFile)
        df['bert'] = df_out['bert']
    else:
        df['bert'] = [None]*len(df)

    nlp = pipeline('sentiment-analysis', model='distilbert-base-uncased', max_length=512, truncation=True)

    # Process the rows in batches, starting from the last checkpoint
    for i in tqdm(range(startRow, len(df), batchSize)):
        endRow = min(i + batchSize, len(df))
        for j in range(i, endRow):
            if pd.isna(df.loc[j, 'bert']):
                result = nlp(str(df.loc[j, 'lyrics']))[0]
                df.loc[j, 'bert'] = -result['score'] if result['label'] == 'NEGATIVE' else result['score']
        df.to_csv(outputFile, index=False)


        # Update the checkpoint
        with open(checkpointFile, 'w') as f:
            f.write(str(endRow))

def addFlairCheckpoint(inputFilePath, outputFile="withFlair.csv", checkpointFile="flair_checkpoint.txt", batchSize=20):
    # Initialize the checkpoint
    if os.path.exists(checkpointFile):
        with open(checkpointFile, 'r') as f:
            checkpoint = f.read()
            startRow = int(checkpoint or 0)
    else:
        startRow = 0

    df = pd.read_csv(inputFilePath)

    # If output file exists, read it and get the 'flair' column. Otherwise, initialize 'flair' column with None.
    if os.path.exists(outputFile):
        df_out = pd.read_csv(outputFile)
        df['flair'] = df_out['flair']
    else:
        df['flair'] = [None]*len(df)

    # Load the pre-trained sentiment analysis model
    classifier = TextClassifier.load('sentiment')

    # Process the rows in batches, starting from the last checkpoint
    for i in tqdm(range(startRow, len(df), batchSize)):
        endRow = min(i + batchSize, len(df))
        for j in range(i, endRow):
            if pd.isna(df.loc[j, 'flair']):
                text = str(df.loc[j, 'lyrics'])
                sentence = Sentence(text)
                classifier.predict(sentence)
                sentiment_label = sentence.labels[0].value
                sentiment_score = sentence.labels[0].score
                df.loc[j, 'flair'] = sentiment_score if sentiment_label == 'POSITIVE' else -sentiment_score
        df.to_csv(outputFile, index=False)

        # Update the checkpoint
        with open(checkpointFile, 'w') as f:
            f.write(str(endRow))


def main():
    # addVader("data/popularityLyrics.csv")
    # addTextBlob("withVader.csv")
    # addFlairCheckpoint("withTextBlob.csv")
    addBertCheckpoint("withFlair.csv")
    

if __name__ == "__main__":
    main()
