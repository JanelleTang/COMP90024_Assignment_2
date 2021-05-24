# ============= COMP90024 - Assignment 2 ============= #
#                               
# The University of Melbourne           
# Team 37
#
# ** Authors: **
# 
# JJ Burke              1048105
# Janelle Tang          694209
# Shuang Qiu            980433
# Declan Baird-Watson   640975
# Avinash Rao           1024577 
# 
# Location: Melbourne
# ==================================================== 
import tweepy
import json
from time import sleep
import geopandas
import geopy
import sys
import os
from shapely.geometry import Point, Polygon
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderUnavailable
from datetime import datetime
import re
from geopy.extra.rate_limiter import RateLimiter
from user_crawler import main as crawler_main
import pandas as pd
from uploader import upload


#needs python 3.6

#this is student 4
consumer_key='c1eQif3Bf37s1MriPv6rb5yET' 
consumer_secret='ze9lyMzHM6H0yyne1LkfduvpfNJ9seAL9clhAtPAZx3T4KruIp'
access_token='1384342701861007364-llYZOhRfo5G7J7O8pygCaO6W6wZfS2'
access_token_secret='d2yR54mrpeXiwau2zZgb4SMuObAPCpR2TInUROPxpZN3X'

sleepTimer = 5

def processTweets(listTweets):
    processed_tweets = []
    if not listTweets:
        return None
    for tweet in listTweets:
        if tweet['user location']:
            locator = geopy.Nominatim(user_agent='myGeocoder')
            cities = ['sydney', 'melbourne', 'brisbane']

            found = False
            for city in cities:
                if re.search(city, tweet['user location'].lower()):
                    processed_tweets.append(tweet)
                    found = True
                    break

            if found:
                continue
            if tweet['user location'].lower() == 'australia' or tweet['user location'].lower() == 'aus':
                continue
            try:
                location = locator.geocode(tweet['user location'], viewbox= [(-10.5, 110.99), (-44.43, 157.87)]) 
            except GeocoderTimedOut as e:
                print("Geocoder TimedOut... sleeping 5")
                sleep(5)

                continue
            except GeocoderUnavailable as e:
                print("Geocoder Unavailable.... sleeping 5")
                sleep(5)
 
            except Exception as e:
                print('caught geocode error')
                print(e)
                continue
            if not location:
                continue
            point = Point(location.latitude, location.longitude)
            coords = [(-11,112),(-11,154),(-44,112),(-44,154)]
            poly = Polygon(coords)
            
            if poly.contains(point):
                processed_tweets.append(tweet)

    return processed_tweets


def sendTweets(tweets_for_submission):
    if tweets_for_submission:
        tweet_lst = []
        for tweet in tweets_for_submission:
            t = {"id": str(tweet['tweet id']), 
                "text":tweet["text"], 
                "location":tweet["user location"], 
                "hashtags":tweet["hashtags"],
                "date_created":tweet['created at']}
            print(str(tweet['tweet id']))
            if not tweet["geo"] or len(tweet["geo"]) == 0:
                t["geo"] = ""
            tweet_lst.append(t)

        print("number of tweets: " + str(len(tweet_lst)))
        response = upload({"data": tweet_lst},'/api/tweet/raw/create') 
        print(response.text)

        now = datetime.now()

        print("Australia tweets appended at: " + str(now))
    else:
        print('no aus tweets appended')

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

class StdOutListener(tweepy.StreamListener):
    def __init__(self,api=None,batch_size=10):
        super().__init__(api)
        ## initialize with a list to store batches of tweets in
        self.tweets = []
        self.batch_size = batch_size
    
    def on_data(self,data):
        try:
            res = json.loads(data)
            temp_dict = {'tweet id': res['id'], 'user id': res['user']['id'], 'user name': res['user']['name'], 
            'screen name': res['user']['screen_name'], 'followers count': res['user']['followers_count'], 
            'user location': res['user']['location'], 'geo': res['geo'], 'created at': str(res['created_at']), 
            'text': res['text'], 'truncated': res['truncated'], 'hashtags': []}

            if res['truncated']:
                temp_dict['text']= res['extended_tweet']['full_text']
            if res['entities']['hashtags']:
                for hashtag in res['entities']['hashtags']:
                    temp_dict['hashtags'].append(hashtag['text'])
                    #print('HASHTAGs: ' + hashtag['text'])
 
                #print('we found no hashtags: ' + temp_dict['text'])

            
            self.tweets.append(temp_dict)

            if len(self.tweets) <= self.batch_size:
                return True
            ## if specified batch has been reached, end stream to call methods on data and insert to couchdb
            return False    

            
        
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        except Exception as e:
            print(e)
        
    def on_error(self, status):
        if status == 420:
            print(status)
            return False
        print('status == 420 did not pick up this error. Here it is though')
        print(status)
        return False

    def clear_tweets(self):
        self.tweets = []

    def return_tweets(self):
        return self.tweets

        
if __name__=='__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = tweepy.Stream(auth, l, )
    arguments = ['climate change', 'climatechange', 'global warming', 'cimateaction', 'climate action', 'globalwarming']

    while True:
        print('about to start stream')
        stream.filter(track=arguments,languages=['en','english'])  
        processedTweets = processTweets(l.return_tweets())
        if not processedTweets:
            l.clear_tweets()
            print('no aus tweets found')
            continue

        print('tweets found good luck - about to fetch historic tweets from user timeline')
        user_IDs = []
        for tweet in processedTweets:
            user_IDs.append(tweet['user id'])
        user_IDs = list(set(user_IDs))
        fetched_user_tweets = crawler_main(user_IDs)
        print('finished fetching tweets from user profile')
        processedTweets.extend(fetched_user_tweets)

        sendTweets(processedTweets)
        l.clear_tweets()


