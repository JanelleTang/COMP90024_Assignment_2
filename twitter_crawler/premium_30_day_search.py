import tweepy
import json
import pandas as pd
from time import sleep
import copy
from datetime import datetime
import os

#testing premium

consumer_key = 'gqeaPMcHDSiBP2DDrKIj14oJ4'
consumer_secret ='EEcwBh5pUPXbtMzHOzIbowIa3jwlFB929UTAK7xBVvyyUjNAM3'
access_token = '1384728716828282886-wYaaBcTYOlOYFoZeMHFSt6A5NCyDb7'
access_token_secret = 'pVBHMmbRd8iV8Njj8Tuo52wsc8sGZKsPEU2vaRwEqgZ0I'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

kwargs = {
    
    #'query': 'ClimateChange place: Melbourne',
    #'query': 'climate change OR climatechange OR #climatechange OR global warming OR globalwarming OR #globalwarming OR climateaction OR climate action OR #climateaction lang:en point_radius:[144.952 -37.806 10.0km]',
    #point_radius not working results from all over world...
    #note query is case in-sensitive
    'query': '(climate change OR climatechange OR #climatechange OR global warming OR globalwarming OR #globalwarming OR climateaction OR climate action OR #climateaction) lang:en (place:melbourne OR place:"Melbourne Australia")',

    'maxResults': 10 #max results must be between 10 and 100
}

#'environment_name': 'searchingTweets',
#'query': 'ClimateChange place:Melbourne Australia'



def sendTweets(tweets_for_submission):
    
    if tweets_for_submission:
        if os.path.isfile('premTweetDump.txt') and os.path.getsize('premTweetDump.txt') > 0:
            with open('premTweetDump.txt') as file:
                data = json.load(file)
                data.extend(tweets_for_submission)
                file.close()

                with open('premTweetDump.txt', 'w') as outfile:
                    tweet_df = pd.DataFrame(data)
                    json.dump(data, outfile, indent=4)
                    outfile.close()
                    tweet_df = tweet_df.drop_duplicates(subset='tweet id')
                    tweet_df.reset_index(inplace=True, drop=True)
                    title = 'premium search ' + str(datetime.now())[:17] + '.xlsx'
                    tweet_df.to_excel(title, index = False)
        else:
            with open('premTweetDump.txt', 'w') as outfile:
                json.dump(tweets_for_submission, outfile, indent=4)
                outfile.close()
                tweet_df = tweet_df.drop_duplicates(subset='tweet id')
                tweet_df.reset_index(inplace=True, drop=True)
                title = 'premium search ' + str(datetime.now())[:17] + '.xlsx'
                tweet_df.to_excel(title, index = False)



def processTweets(tweets):
    processedTweets = []
    for tweet in tweets:
        temp_dict = {'tweet id': tweet.id, 'user id': tweet.user.id, 'text': tweet.text, 'lang': tweet.lang, 'user location': tweet.user.location, 
        'user geo_enabled': tweet.user.geo_enabled, 'coordinates': tweet.coordinates, 'created_at': str(tweet.created_at)}

        #status object can't get full tweet text if truncated
        processedTweets.append(temp_dict)
    return processedTweets
        
    

def main():
    tweets = api.search_30_day(environment_name='searchingTweets', **kwargs) 
    processedTweets = processTweets(tweets)
    sendTweets(processedTweets)

main()
