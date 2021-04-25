import tweepy
import json
import pandas as pd
from time import sleep

consumer_key='gqeaPMcHDSiBP2DDrKIj14oJ4'
consumer_secret='EEcwBh5pUPXbtMzHOzIbowIa3jwlFB929UTAK7xBVvyyUjNAM3'
access_token='1384728716828282886-wYaaBcTYOlOYFoZeMHFSt6A5NCyDb7'
access_token_secret='pVBHMmbRd8iV8Njj8Tuo52wsc8sGZKsPEU2vaRwEqgZ0I'

'''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
'''

'''
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)


user = api.get_user('twitter')
print(user.screen_name)
print(user.followers_count)
for friend in user.friends():
   print(friend.screen_name)'''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)
tweet_count = 0
count_per_search = 1
max_tweet_harvested = 5
max_search_count = 2
tweet_df = pd.DataFrame(columns=['tweet id','user id','text','lang','user location','user geo_enabled','coordinates'])
tweet_id = 105821868070932483

def get_tweet(query, count_per_search, language, geocoordinates,tweet_id):
    tweets = api.search(q=query, count=count_per_search, lang=language, geocode=geocoordinates, since_id = tweet_id)
    for tweet in tweets:
        temp_dict = {'tweet id': tweet.id, 'user id': tweet.user.id, 'text': tweet.text, 'lang': tweet.lang, 'user location': tweet.user.location, 'user geo_enabled': tweet.user.geo_enabled, 'coordinates': tweet.coordinates}
        tweet_df = tweet_df.append(temp_dict, ignore_index=True)
        print('appended')
        print(temp_dict)

        tweet_id = tweet.id
    return tweet_id


while tweet_count <= max_tweet_harvested:
    small_count = 0
    while small_count <= max_search_count:
        tweet_id = get_tweet("*", count_per_search, 'en', '-37.81160107129726,144.96246427028737,20km', tweet_id + 1)
        small_count +=1  

        
    print(tweet_df.to_string())
    tweet_count += max_search_count
    sleep(5)
    



#for page in tweepy.Cursor(api.search, q='python', count=5, tweet_mode='extended').pages():
    #print(page)
#tweet_return = tweepy.API.search('melbourne', count=2)

#for tweet in tweet_return:
    #print(tweet)


'''
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')

#session.set('request_token', auth.request_token['oauth_token'])
verifier = request.GET.get('oauth_verifier')
'''


'''
# Let's say this is a web app, so we need to re-build the auth handler
# first...
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
token = session.get('request_token')
session.delete('request_token')
auth.request_token = { 'oauth_token' : token,
                         'oauth_token_secret' : verifier }

try:
    auth.get_access_token(verifier)
except tweepy.TweepError:
    print('Error! Failed to get access token.')
'''
