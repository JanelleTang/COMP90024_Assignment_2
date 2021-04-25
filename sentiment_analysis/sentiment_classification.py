import json
import ijson
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

text_filepath = 'data/smallTwitter.json'

def extract_json(filename):
    data = []
    with open(filename, 'r') as f:
        obj = ijson.items(f, 'rows.item.value')
        #cols = [['geometry','coordinates'],['properties','text']]
        cols = [['properties','text']]
        for row in obj:
            tweet_data=[]
            for colgroup in cols:
                temp_row = row
                for col in colgroup:
                    temp_row = temp_row[col]
                tweet_data.append(temp_row)
            data.append(tweet_data[0])
    return data

def get_sentiment(lst):
    sia = SentimentIntensityAnalyzer()
    sentiment_lst = []
    for text in lst:
        sentiment_lst.append([text,sia.polarity_scores(text)])
    df = pd.DataFrame(sentiment_lst,columns = ['text','sentiment_dict'])
    df = expand_dict_column(df,'sentiment_dict')
    return df

def expand_dict_column(df,col):
    df1 = pd.DataFrame.from_dict(df[col].tolist())
    return df.drop(col,axis=1).join(df1,rsuffix='_'+col)

text_data = extract_json(text_filepath)
print(get_sentiment(text_data[:10]))