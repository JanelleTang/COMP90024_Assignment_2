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
import pandas as pd
from time import sleep
import copy
from datetime import datetime
#pip install openpyxl

def processTweet(tweet, geocoordinate):
    geocoordSplit = geocoordinate.split(',')

    temp_dict = {'tweet id': tweet.id, 'user id': tweet.user.id, 'text': tweet.text, 'lang': tweet.lang, 'user location': tweet.user.location, 
    'user geo_enabled': tweet.user.geo_enabled, 'coordinates': tweet.coordinates, 'created_at': tweet.created_at, 'latlong' : str(geocoordSplit[0] + ',' + geocoordSplit[1]),
    'search_radius': geocoordSplit[2]}

    return temp_dict


def searchTweets(query, twitter_count, language, geocoordinate, api):
    tweets = api.search(q=query, count=twitter_count, lang=language, geocode=geocoordinate)
    tweet_data = []
    for tweet in tweets:
        if not tweet.id:
            continue
        temp_dict = processTweet(tweet, geocoordinate)
        tweet_data.append(temp_dict)
    return tweet_data
    

def readKeys():
    f = open("keys_tokens.txt", "r")
    keys_tokens = eval(f.read())
    #student_1 (Declan)
    #student_2 (Janelle)
    #Student_3 (Shuang)
    #student_4 (JJ)

    return keys_tokens

def readCityCoords():
    f = open("Australian_cities_coordinates.txt", "r")
    cityCoordsDict = eval(f.read())
    cityList = cityCoordsDict.keys()

    return cityCoordsDict, cityList


def setUser(keys_tokens, user_no):
    total_users = len(keys_tokens)
    user = user_no % total_users
    consumer_key = keys_tokens[user][1]
    consumer_secret= keys_tokens[user][2]
    access_token = keys_tokens[user][3]
    access_token_secret = keys_tokens[user][4]

    return consumer_key, consumer_secret, access_token, access_token_secret


def createGridPoints(city, search_radius, cityCoordsDict):
    interval = 0.05 #approx 5km
    oglat = cityCoordsDict[city][0]
    oglong = cityCoordsDict[city][1]
    templong = copy.deepcopy(oglong)
    latlong_list = []

    for i in range(1,16):
        for j in range(1,16):
            templong += interval
            tempcoord = str(oglat) +',' + str(templong) + ',' + str(search_radius) + 'km'
            latlong_list.append(tempcoord)
        oglat -=interval
        templong = copy.deepcopy(oglong)
    
    return latlong_list

def checkWait(student_no, keys_tokens):
    total_users = len(keys_tokens)
    if student_no % total_users == 0:
        sleep(.5)

def harvestTweets(city, cityCoordsDict, keys_tokens, tweet_count, query, language):
    tweet_df = pd.DataFrame(columns=['tweet id','user id','text','lang','user location','user geo_enabled','coordinates','created_at','latlong','search_radius'])
    search_radius = 5 #km
    grid_points = createGridPoints(city, search_radius, cityCoordsDict)
    student_no = 0
    all_tweet_data = []

    for point in grid_points:
        checkWait(student_no, keys_tokens)
        consumer_key, consumer_secret, access_token, access_token_secret = setUser(keys_tokens, student_no)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        tweet_data = searchTweets(query, tweet_count, language, point, api)
        #print(str(point)) #testing reasons, delete
        
        if tweet_data: #if tweet data found append it
            all_tweet_data.append(tweet_data)
        student_no += 1
    
    for item in all_tweet_data:
        tweet_df = tweet_df.append(item,ignore_index=True)
        
    tweet_df = tweet_df.drop_duplicates(subset='tweet id')
    tweet_df.reset_index(inplace=True, drop=True)
    
    print(tweet_df.to_string())
    title = 'tweet search melb dump ' + str(datetime.now())[:17] + '.xlsx'
    tweet_df.to_excel(title, index = False)

    

def main():
    cityCoordsDict, cityList = readCityCoords()
    keys_tokens = readKeys()
    tweet_count = 200
    query = ('climate change OR climatechange OR #climatechange OR Climate Change OR #ClimateChange OR Climate change OR CLIMATE CHANGE OR GLOBAL WARMING OR Global Warming OR Global warming OR global warming OR climateaction OR Climate Action OR CLIMATE ACTIOn OR Climate action')
    query = ('the')
    language = 'en'

    for city in cityList:
        harvestTweets(city, cityCoordsDict, keys_tokens, tweet_count, query, language)

    
main()


