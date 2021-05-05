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

userIDs = [1253072343804469248, 3834645913, 733983882, 103809511, 1052354553750814720, 16834659]

def receiveUserIDs():
    a = 1
    #insert receiving code

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
            print('FOUND A RELEVENT TWEET')
            return True
    return False


def processTweets(tweets):
    processed_tweets = []
    for tweet in tweets:
        if not tweet.id:
            continue
        temp_dict = {'tweet id': tweet.id, 'user id': tweet.user.id, 'text': tweet.text, 'lang': tweet.lang, 'user location': tweet.user.location, 
        'user geo_enabled': tweet.user.geo_enabled, 'coordinates': tweet.coordinates, 'created_at': tweet.created_at}
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
        print(processed_tweets)
        return processed_tweets

def harvestTweets(api, userIDs):
    final_tweets = []

    for userID in userIDs:
        tweets_found = searchTweets(api, userID)
        if tweets_found:
            final_tweets.extend(tweets_found)


def main():
    consumer_key = 'gb66mKjCEv70Wyk8R9IOHw24F'
    consumer_secret ='TFc1oMo5hkDVsxcwTCjYhTGvzt68mIm4uzsanlJK0WFsJNdpRi'
    access_token = '1385438387054596098-iW8kTEeFOzCBHQnHSuUF0KfDiBdq2L'
    access_token_secret = 'VvHR7tUgIY8h7airxseHPGSEwToYRhAjNiQ8Danr4iUTT'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    receiveUserIDs()
    keys_tokens = readKeys()
    harvestTweets(api, userIDs)


main()