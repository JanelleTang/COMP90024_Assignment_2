import tweepy
import json
import pandas as pd
from time import sleep
import copy
from datetime import datetime
import geopandas
import geopy
import sys
import os
from shapely.geometry import Point, Polygon
from geopy.exc import GeocoderTimedOut
from datetime import datetime
import re

def receiveUserIDs():
    ID_list = []
    with open('premHistFinalTweetsProcessed.json') as file:
        data = json.load(file)
        file.close()

    for tweet in data:
        ID_list.append(tweet['user id'])

    ID_list = list(set(ID_list))

    #if os.path.isfile('userCrawlerData.txt') and os.path.getsize('userCrawlerData.txt') > 0:
        #with open('userCrawlerData.txt') as file:
            #data = json.load(file)
            #file.close()
            #for tweet in data:
                #if tweet['user id'] in ID_list:
                    #ID_list.remove(tweet['user id'])
    
    return ID_list

def readKeys():
    f = open("keys_tokens.txt", "r")
    keys_tokens = eval(f.read())
    #student_1 (Declan)
    #student_2 (Janelle)
    #Student_3 (Shuang)
    #student_4 (JJ)

    return keys_tokens

def tweetRelevent(tweet):
    relevent = False
    keywords = ['climate change', 'climatechange', 'climate action', 'climateaction', 'global warming','globalwarming']

    for keyword in keywords:
        if re.search(keyword, tweet['text'].lower()):
            return True
    return False


def processTweets(tweets):
    processed_tweets = []
    for tweet in tweets:
        if not tweet.id:
            continue
        temp_dict = {'tweet id': tweet.id, 'user id': tweet.user.id, 'text': tweet.text, 'lang': tweet.lang, 'user location': tweet.user.location, 
        'user geo_enabled': tweet.user.geo_enabled, 'coordinates': tweet.coordinates, 'created_at': tweet.created_at, 'hashtags': []}
        if tweet.entities['hashtags']:
            for hashtag in tweet.entities['hashtags']:
                temp_dict['hashtags'].append(hashtag['text'])
        else:
            print('we found no hashtags???? text: ' + tweet.text)
        if not tweetRelevent(temp_dict):
            continue
        processed_tweets.append(temp_dict)
    return processed_tweets


def searchTweets(api, userID):
    try:
        tweets = api.user_timeline(id=userID, count=1000)
        processed_tweets = processTweets(tweets)
    except Exception as e:
        print(e)
        return None
    if processed_tweets:
        return processed_tweets

def sendTweets(tweets_for_submission):
    if tweets_for_submission:
        if os.path.isfile('userCrawlerDatav2.txt') and os.path.getsize('userCrawlerDatav2.txt') > 0:
            with open('userCrawlerDatav2.txt') as file:
                data = json.load(file)
                data.extend(tweets_for_submission)
                file.close()

                with open('userCrawlerDatav2.txt', 'w') as outfile:
                    tweet_df = pd.DataFrame(data)
                    json.dump(data, outfile, indent=4, default=str)
                    outfile.close()
                    tweet_df = tweet_df.drop_duplicates(subset='tweet id')
                    tweet_df.reset_index(inplace=True, drop=True)
                    #title = 'premium search hist prem' + str(datetime.now())[:17] + '.xlsx'
                    tweet_df.to_excel('userCrawlerDumpv2.xlsx', index = False)
        else:
            with open('userCrawlerDatav2.txt', 'w') as outfile:
                tweet_df = pd.DataFrame(tweets_for_submission)
                json.dump(tweets_for_submission, outfile, indent=4, default=str)
                outfile.close()
                tweet_df = tweet_df.drop_duplicates(subset='tweet id')
                tweet_df.reset_index(inplace=True, drop=True)
                #title = 'premium search hist ' + str(datetime.now())[:17] + '.xlsx'
                tweet_df.to_excel('userCrawlerDumpv2.xlsx', index = False)


def harvestTweets(api, userIDs): #insert USERID
    final_tweets = []

    for userID in userIDs:
        tweets_found = searchTweets(api, userID)
        if tweets_found:
            #sendTweets(tweets_found) #remove in final
            final_tweets.extend(tweets_found)
    return final_tweets


def main(ID_list): #insert ID_list here
    consumer_key = 'gb66mKjCEv70Wyk8R9IOHw24F'
    consumer_secret ='TFc1oMo5hkDVsxcwTCjYhTGvzt68mIm4uzsanlJK0WFsJNdpRi'
    access_token = '1385438387054596098-iW8kTEeFOzCBHQnHSuUF0KfDiBdq2L'
    access_token_secret = 'VvHR7tUgIY8h7airxseHPGSEwToYRhAjNiQ8Danr4iUTT'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return harvestTweets(api, ID_list)

