import os
import json
import time
import requests
import datetime
import dateutil
import pandas as pd
from dateutil.relativedelta import relativedelta

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from textblob import TextBlob

# import textrazor

# from transformers import pipeline


# import opinion_finder

# import torch
# from transformers import BertTokenizer, BertForSequenceClassification

# from flair.models import TextClassifier
# from flair.data import Sentence

# from polyglot.detect import Detector
# from polyglot.text import Text



#BOTTLENECK: 10 requests per minute, 4000 requests per day

# 1 request = top 10 most viewed articles
# Per day for 4 years -> 365 * 4 = 1460 total requests (146 minutes to run = 2.5 hrs)
#   Also possible to do on full text, but that's a lot of data. (622 words on average * 14600 articles = 9 million words)
#   Also possible to do snippets/first paragraph but that leads to inconsistent results.

# TODO - 1. get 10 most popular articles per day (using popular api, not archives api) (somehow ensure America only)
# 2. get full text for each article, not just headline/abstract (HOW?)
# 3. remove stopwords, preprocessing
# 4. perform SA (with numerous tools) on headline+abstract+fulltext
# 5. combine into master .csv
# 6. visualize results

# Questions: most popular =  most emailed, most shared, or most viewed? (use most viewed)
# Should I include/exclude certain sections (e.g. sports, opinion, etc.)? If so need to integrate two databases. (exclude obituaries)
# Should I run SA on full text or just headline/abstract? (full text means much more data but also more accurate)


end = datetime.date(2021, 12, 31) # Dec 31 2020
start = end - relativedelta(months = 1) # Jan 2016

def send_request(date):
    base_url = 'https://api.nytimes.com/svc/archive/v1/'
    private_key = "ZTDuHtMacPzfve7f7GZ7obg1TTGZ8myp"
    url = base_url + '/' + date[0] + '/' + date[1] + '.json?api-key=' + private_key
    response = requests.get(url).json()
    time.sleep(6) # 10 requests per minute = 1 request every 6 seconds (7 to be safe)
    return response


def is_valid(article, date):
    in_range = date > start and date < end
    has_headline = type(article['headline']) == dict and 'main' in article['headline'].keys()
    return in_range and has_headline


def parse_response(response):
    data = {'headline': [],  
        'date': [], 
        'vader_SA': [],
        'textblob_SA' : [],
       # 'textrazor_SA' : [], # Hugging Face Transformers
        'section': [],
        'abstract': [],
        'keywords': [],
        'url': [],
        'doc_type': [],
        'material_type': [],
        'vader_full': [], # compound, negative, neutral, positive'

        }
    try:
        articles = response['response']['docs']
    except KeyError:
        print('Error: ')
        return
    for article in articles:
        date = dateutil.parser.parse(article['pub_date']).date()
        if is_valid(article, date):
            data['date'].append(date)
            data['headline'].append(article['headline']['main'])
            data['url'].append(article['web_url'])
            data['section'].append(article['section_name']) 
            if 'abstract' in article:
                data['abstract'].append(article['abstract'])
            else:
                data['abstract'].append(None)
            data['doc_type'].append(article['document_type'])
            if 'type_of_material' in article: 
                data['material_type'].append(article['type_of_material'])
            else:
                data['material_type'].append(None)
            keywords = [keyword['value'] for keyword in article['keywords'] if keyword['name'] == 'subject']
            data['keywords'].append(keywords)

            # opinion_finder = opinion_finder.OpinionFinder()
            # opinion_scores = opinion_finder.get_opinion_scores(str(article['headline']) + ' ' + article['abstract']) # what SA is being performed on
            # data['OpinionFinder'].append(opinion_scores)

            text = str(article['headline']) + ' ' + str(article['abstract'])
            
            sid = SentimentIntensityAnalyzer()
            nltk_sentiment_score = sid.polarity_scores(text)
            data['vader_full'].append(nltk_sentiment_score)
            data['vader_SA'].append(nltk_sentiment_score['compound'])

            blob = TextBlob(text)
            data['textblob_SA'].append(blob.sentiment.polarity)

            # # Load the pre-trained tokenizer and model for sentiment analysis
            # tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            # model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

            # text_obj = Text(text, hint_language_code = 'en')
            # data['polyglot_SA'].append(text_obj.polarity)

            # sentiment_classifier = pipeline("sentiment-analysis")
            # result = sentiment_classifier(text)[0]
            # data['HFT_SA'].append(result['score'])

            # client = textrazor.TextRazor("27258e3285b1f8b0cc975add3f8ff92a5d2f266f3bb96cdba92e7d62")
            # response = client.analyze(text)
            # data['textrazor_SA'].append(response.sentiment_score)  

    return pd.DataFrame(data) 


def get_data(dates):
    '''Sends and parses request/response to/from NYT Archive API for given dates.'''
    total = 0
    print('Date range: ' + str(dates[0]) + ' to ' + str(dates[-1]))
    if not os.path.exists('headlines'):
        os.mkdir('headlines')
    for date in dates:
        response = send_request(date)
        df = parse_response(response)
        if df is not None:
            total += len(df)
            df.to_csv('headlines/' + date[0] + '-' + date[1] + '.csv', index=False)
            print('Saving headlines/' + date[0] + '-' + date[1] + '.csv...')
        else:
            print("date " + date[0] + '-' + date[1] + " is empty")
    print('Number of articles collected: ' + str(total))

def main():
    months_in_range = [x.split(' ') for x in pd.date_range(start, end, freq='MS').strftime("%Y %-m").tolist()]
    get_data(months_in_range)

if __name__ == "__main__":
    main()