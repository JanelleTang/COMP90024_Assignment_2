from uploader import upload
import os
import ujson

data = None
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'tweetDump.json')
with open(my_file) as file:
    data = ujson.load(file)

# parse and preprocess the tweets
tweets = []
for tweet in data:
    t = {"id": tweet['tweet id'], "text":tweet["text"], "location":tweet["user location"], "hashtags":tweet["hashtags"]}
    if tweet["geo"] == None:
        t["geo"] = ""
    tweets.append(t)
response = upload(tweets, "/api/tweet/raw/create")
print(response)
