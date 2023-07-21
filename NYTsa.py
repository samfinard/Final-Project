import os
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

end = datetime.date(2021, 12, 31) # Dec 31 2021
start = end - relativedelta(years = 5) # Jan 2017

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
    data = {
        'date': [], 
        'headline': [],  
        'abstract': [],
        'url': [],
        'vader_SA': [],
        'textblob_SA' : [],
        
        # 'section': [],
        # 'keywords': [],
        # 'doc_type': [],
        # 'material_type': [],
        # 'vader_full': [], # compound, negative, neutral, positive'
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
            data['abstract'].append(article['abstract'])
            # data['section'].append(article['section_name'])
            # data['doc_type'].append(article['document_type'])
            # data['material_type'].append(article['type_of_material'])
            # keywords = [keyword['value'] for keyword in article['keywords'] if keyword['name'] == 'subject']
            # data['keywords'].append(keywords)

            text = str(article['headline']) + ' ' + str(article['abstract'])
            
            data['vader_SA'].append(get_vader_SA(text))
            data['textblob_SA'].append(get_textblob_SA(text))


    return pd.DataFrame(data) 

def get_vader_SA(text):
    sid = SentimentIntensityAnalyzer()
    nltk_sentiment_score = sid.polarity_scores(text)
    return nltk_sentiment_score['compound']

def get_textblob_SA(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def get_data(dates):
    total = 0
    print('Date range: ' + str(dates[0]) + ' to ' + str(dates[-1]))
    if not os.path.exists('articles'):
        os.mkdir('articles')
    for date in dates:
        response = send_request(date)
        df = parse_response(response)
        if df is not None:
            total += len(df)
            df.to_csv('articles/' + date[0] + '-' + date[1] + '.csv', index=False)
            print('Saving articles/' + date[0] + '-' + date[1] + '.csv...')
        else:
            print("date " + date[0] + '-' + date[1] + " is empty")
    print('Number of articles collected: ' + str(total))

def main():
    months_in_range = [x.split(' ') for x in pd.date_range(start, end, freq='MS').strftime("%Y %-m").tolist()]
    get_data(months_in_range)

if __name__ == "__main__":
    main()