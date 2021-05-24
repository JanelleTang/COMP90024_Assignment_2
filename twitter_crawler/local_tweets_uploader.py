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
from uploader import upload
import os
import ujson

data = None
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'tweet_dump.json')
with open(my_file) as file:
    data = ujson.load(file)

# parse and preprocess the tweets
tweets = []
for tweet in data:
    t = {"id": str(tweet['tweet id']), 
        "text":tweet["text"], 
        "location":tweet["user location"], 
        "hashtags":tweet["hashtags"],
        "date_created":tweet['created at']}
    if not tweet["geo"] or len(tweet["geo"]) == 0:
        t["geo"] = ""
    tweets.append(t)

start = 0
for i in range(len(tweets) // 100):
    response = upload({"data": tweets[start: start + 100]}, "/api/tweet/raw/create")
    start += 100
