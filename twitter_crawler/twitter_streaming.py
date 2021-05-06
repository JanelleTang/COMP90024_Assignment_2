import tweepy
import json
from time import sleep
import geopandas
import geopy
import sys
import os
from shapely.geometry import Point, Polygon
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from datetime import datetime
import re
from geopy.extra.rate_limiter import RateLimiter

consumer_key='gqeaPMcHDSiBP2DDrKIj14oJ4'
consumer_secret='EEcwBh5pUPXbtMzHOzIbowIa3jwlFB929UTAK7xBVvyyUjNAM3'
access_token='1384728716828282886-wYaaBcTYOlOYFoZeMHFSt6A5NCyDb7'
access_token_secret='pVBHMmbRd8iV8Njj8Tuo52wsc8sGZKsPEU2vaRwEqgZ0I'

def processTweets(listTweets):
    processed_tweets = []
    if not listTweets:
        return None
    for tweet in listTweets:
        if tweet['user location']:
            locator = geopy.Nominatim(user_agent='myGeocoder')
            #if tweet['user location'].lower() == 'sydney' or tweet['user location'] == 'Brisbane' or tweet['user location'] == 'Sydney, Australia' or tweet['user location'] == 'Brisbane, Australia' or tweet['user location'] == 'Australia, Sydney' or tweet['user location'] == 'Australia, Brisbane' or tweet['user location'] == 'Brisbane, Queensland' or tweet['user location'] == 'Sydney, New South Wales':
                #processed_tweets.append(tweet)
                #continue
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
            location = None
            try:
                location = locator.geocode(tweet['user location'], viewbox= [(-10.5, 110.99), (-44.43, 157.87)]) 
            except GeocoderTimedOut as e:
                print("Geocoder TimedOut... sleeping 5")
                sleep(5)
                continue
            except GeocoderUnavailable as e:
                print("Geocpder Unavailable.... sleeping 5")
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
        if os.path.isfile('tweetDump.txt') and os.path.getsize('tweetDump.txt') > 0:
            with open('tweetDump.txt') as file:
                data = json.load(file)
                data.extend(tweets_for_submission)
                file.close()

                with open('tweetDump.txt', 'w') as outfile:
                    json.dump(data, outfile)
                    outfile.close()
        else:
            with open('tweetDump.txt', 'w') as outfile:
                json.dump(tweets_for_submission, outfile)
                outfile.close()
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
            'user location': res['user']['location'], 'geo': res['geo'], 'created at': res['created_at'], 
            'text': res['text'], 'truncated': res['truncated'], 'hashtags': []}

            if temp_dict['truncated']:
                temp_dict['text']= res['extended_tweet']['full_text']
            if res['entities']['hashtags']:
                temp_dict['hashtags'] = res['entities']['hashtags']

            
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
            sleep(5)
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
    arguments = ['climate change', 'climatechange', 'global warming', 'cimateaction', 'climate action']

    while True:
        stream.filter(track=arguments,languages=['en','english'])  
        processedTweets = processTweets(l.return_tweets())
        sendTweets(processedTweets)
        l.clear_tweets()

        #now = datetime.now()
        #print('FINISHED A LOOP OF STREAM: ' + str(now))

