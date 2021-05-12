from uploader import upload
from .sentimentAnalysis import CleanTweet

## Write something to do with getting tweets by size 1000 ##

tweets = []
## Processing and aggregating tweets ##
regions_lst = []
for tweet in tweets:
    text = tweet['text']
    if tweet['geo'] != None: ## CHANGE THIS DEPENDING ON EMPTY
        location = tweet['geo']
        geo = True
    else:
        location = tweet['location']
        geo = False
    tweet_obj = CleanTweet(text,location,geo)
    regions_lst.append(tweet_ob.get_dict())
resp = upload(regions_lst,"region/create/")
print(response)