from uploader import upload
from sentiment_analyser import *
import requests
import sys
import argparse

## Processing and aggregating tweets ##
def tweet_processor(tweets):
    regions_lst = []
    for data in tweets:
        for k,tweet in data.items():
            text = tweet['text']
            if tweet['geo'] != "": ## CHANGE THIS DEPENDING ON EMPTY
                location = tweet['geo']
                geo = True
            else:
                location = tweet['location']
                geo = False
            tweet_obj = CleanTweet(text,location,geo)
            region_data = tweet_obj.get_dict()
            if region_data != None:
                regions_lst.append(region_data)
    return {"data":regions_lst}

def regions_dict_uploader(tweets):
    regions_data = tweet_processor(tweets)
    response = upload(regions_data, "/api/location/create")
    print(response)

if __name__ == '__main__':
    path = 'http://127.0.0.1:8000/api/tweet/raw/'
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("size", help="process tweets by size",type=int)
        args = parser.parse_args()
        size = args.size
        tweets = requests.get(path+str(size)).json()['obj']
        regions_dict_uploader(tweets)
    except:
        e = sys.exc_info()[0]
        print(e)
