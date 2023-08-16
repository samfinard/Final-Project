import pandas as pd
import numpy as np

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
from scipy.special import softmax
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

def addBertCheckpoint(inputFilePath, outputFile="withBert.csv", checkpointFile="bert_checkpoint.txt", batchSize=20, window_size=512, stride=512):
    if os.path.exists(checkpointFile):
        with open(checkpointFile, 'r') as f:
            checkpoint = f.read()
            startRow = int(checkpoint or 0)
    else:
        startRow = 0

    df = pd.read_csv(inputFilePath)

    if os.path.exists(outputFile):
        df_out = pd.read_csv(outputFile)
        df['bert'] = df_out['bert']
    else:
        df['bert'] = [None]*len(df)

    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
    model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased', return_dict=True)

    # Move model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    for i in tqdm(range(startRow, len(df), batchSize)):
        endRow = min(i + batchSize, len(df))
        for j in range(i, endRow):
            if pd.isna(df.loc[j, 'bert']):
                lyrics = str(df.loc[j, 'lyrics'])
                segments = [lyrics[k:k+window_size] for k in range(0, len(lyrics), stride)]
                inputs = tokenizer(segments, return_tensors="pt", truncation=False, padding='max_length', max_length=window_size)
                inputs = {key: val.to(device) for key, val in inputs.items()} # Move inputs to GPU if available
                outputs = model(**inputs)
                scores = torch.softmax(outputs.logits, dim=1)
                score = torch.mean(scores, dim=0)[1].item()
                df.loc[j, 'bert'] = score
        df.to_csv(outputFile, index=False)

        with open(checkpointFile, 'w') as f:
            f.write(str(endRow))

def addBertCheckpoint(inputFilePath, outputFile="withBert.csv", checkpointFile="bert_checkpoint.txt", batchSize=20, window_size=510, stride=510):
    if os.path.exists(checkpointFile):
        with open(checkpointFile, 'r') as f:
            checkpoint = f.read()
            startRow = int(checkpoint or 0)
    else:
        startRow = 0

    df = pd.read_csv(inputFilePath)

    if os.path.exists(outputFile):
        df_out = pd.read_csv(outputFile)
        df['bert'] = df_out['bert']
    else:
        df['bert'] = [None]*len(df)

    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
    model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased', return_dict=True)

    # Move model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    for i in tqdm(range(startRow, len(df), batchSize)):
        endRow = min(i + batchSize, len(df))
        for j in range(i, endRow):
            if pd.isna(df.loc[j, 'bert']):
                lyrics = str(df.loc[j, 'lyrics'])
                segments = [lyrics[k:k+window_size] for k in range(0, len(lyrics), stride)]
                inputs = tokenizer(segments, return_tensors="pt", padding=True, truncation=True, max_length=512)
                inputs = {key: val.to(device) for key, val in inputs.items()} # Move inputs to GPU if available
                outputs = model(**inputs)
                scores = torch.softmax(outputs.logits, dim=1)
                score = torch.mean(scores, dim=0)[1].item()
                df.loc[j, 'bert'] = score
        df.to_csv(outputFile, index=False)

        with open(checkpointFile, 'w') as f:
            f.write(str(endRow))

def main():
    # addVader("data/popularityLyrics.csv")
    # addTextBlob("withVader.csv")
    # addFlairCheckpoint("withTextBlob.csv")
    addBertCheckpoint("withFlair.csv")
    

if __name__ == "__main__":
    main()
