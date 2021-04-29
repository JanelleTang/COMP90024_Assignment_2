import tweepy
import json
import pandas as pd
from time import sleep

tweet_df = pd.DataFrame(columns=['tweet id','user id','text','lang','user location','user geo_enabled','coordinates','created_at'])

def harvestTweets(query, twitter_count, language, geocoordinate, api):
    tweets = api.search(q=query, count=twitter_count, lang=language, geocode=geocoordinate)
    tweet_data = []
    for tweet in tweets:
        if not tweet.id:
            continue
        temp_dict = {'tweet id': tweet.id, 'user id': tweet.user.id, 'text': tweet.text, 'lang': tweet.lang, 'user location': tweet.user.location, 
        'user geo_enabled': tweet.user.geo_enabled, 'coordinates': tweet.coordinates, 'created_at': tweet.created_at}
        tweet_data.append(temp_dict)
    return tweet_data
    

def readKeys():
    f = open("keys_tokens.txt", "r")
    keys_tokens = eval(f.read())
    #student_1 (Declan)
    #student_2 (Janelle)
    #Student_3 (Shuang)

    return keys_tokens

def setUser(key, keys_tokens):

    consumer_key = keys_tokens[key]
    consumer_secret= keys_tokens[key]
    access_token = keys_tokens[key]
    access_token_secret = keys_tokens[key]
    return consumer_key, consumer_secret, access_token, access_token_secret



def main():
    keys_tokens = readKeys()
    #melb geocoordinats 
    geocoordinates = ['-37.68659979189392, 144.69409095162106, 10km', '-37.76161761121927, 145.05212437223904, 10km', '-37.962851247212704, 145.16119415614054, 10km']
    while True:
        student_no = 0
        for key in keys_tokens.keys():
            consumer_key, consumer_secret, access_token, access_token_secret = setUser(key, keys_tokens)
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            api = tweepy.API(auth)
            tweet_count = 5
            query = "*"
            language = 'en'
            geocoordinate = geocoordinates[student_no]
            tweet_data = harvestTweets(query, tweet_count, language, geocoordinate, api)
            tweet_df = tweet_df.append(tweet_data,ignore_index=True)
            print(tweet_df.to_string())
            student_no += 1
        break


main()


