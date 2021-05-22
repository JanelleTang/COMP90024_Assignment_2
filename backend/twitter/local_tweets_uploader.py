from uploader import upload
import os
import ujson

data = None
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'static_tweets_outv3.json')
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
    if not tweet["geo"]:
        t["geo"] = ""
    tweets.append(t)
tweets = {"data":tweets}
response = upload(tweets, "/api/tweet/raw/create")
print(response)
