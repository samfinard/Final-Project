import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
from tqdm.notebook import tqdm
from tqdm import tqdm
tqdm.pandas()
import nltk
# nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import tensorflow as tf
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline



def classify_emotion(text):
    # model_name = "cardiffnlp/twitter-roberta-base-emotion"
    model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
    inputs = tokenizer.encode(text, return_tensors='pt')
    outputs = model(inputs)
    probs = torch.nn.functional.softmax(outputs[0], dim=-1)
    categories = ['anger', 'joy', 'optimism', 'sadness', 'anxious']
    
    return categories[torch.argmax(probs)]

def bert(text):
    nlp = pipeline('sentiment-analysis')
    return nlp(text)[0]


# Function for NLTK
def get_nltk(text):
    sia = SentimentIntensityAnalyzer()
    polarity = sia.polarity_scores(text)
    return polarity

# Function for TextBlob
def textblob(text):
    testimonial = TextBlob(text)
    polarity = testimonial.sentiment.polarity
    return polarity


def addVader(inputFilePath):
    df = pd.read_csv(inputFilePath)
    sia = SentimentIntensityAnalyzer()
    df['vader'] = df.progress_apply(lambda row: sia.polarity_scores(str(row['headline']) + ' ' + str(row['abstract']))['compound'], axis=1)
    df.to_csv("NYTarticles_all_vader.csv", index=False)

def addBert(inputFilePath):
    df = pd.read_csv(inputFilePath)
    nlp = pipeline('sentiment-analysis')
    df['bert'] = df.progress_apply(lambda row: nlp(str(row['headline']) + ' ' + str(row['abstract']))[0]['score'], axis=1)
    df['bert'] = df['bert'].apply(lambda x: -x['score'] if x['label'] == 'NEGATIVE' else x['score'])

    df.to_csv("NYTarticles_all_vader_bert.csv", index=False)

def addTextBlob(inputFilePath):
    df = pd.read_csv(inputFilePath)
    df['textblob'] = df.progress_apply(lambda row: TextBlob(str(row['headline']) + ' ' + str(row['abstract'])).sentiment.polarity, axis=1)
    df.to_csv("NYTarticles_all_vader_textblob.csv", index=False)


def main():
    # filepath = "../data/NYTarticles_all.csv"
    # addVader(filepath)
    filepath = "NYTarticles_all_vader_textblob.csv"
    # addTextBlob(filepath)
    addBert("NYTarticles_all_vader.csv")
    
    # addTextBlob("NYTarticles_all_vader.csv")
    
    # df = pd.read_csv(filepath)
    # print(df.columns.tolist())
    # print(bert("test"))
    
    # text = "Testing the sentiment analysis. I am very anxious.."
    # print("nltk: ", get_nltk(text))
    # print("textblob: ", textblob(text))
    # print("vader: ", vader(text))
    # print("bert: ", bert(text))
    # print("classify_emotion: ", classify_emotion(text))

if __name__ == "__main__":
    main()
