import os
import json
import couchdb


couch = couchdb.Server() #This gets you a Server object, representing a CouchDB server. By default, it assumes CouchDB is running on localhost:5984. 
couch.resource.credentials = ('admin', 'alexander94')

if 'shuang_db' in couch:
    print('shuang_db in couch server')
    db = couch['shuang_db']
else:
    print('shuang_db not in couch server. Creating database')
    db = couch.create('shuang_db')


if os.path.isfile('tweetDump.txt') and os.path.getsize('tweetDump.txt') > 0:
    with open('tweetDump.txt') as file:
        data = json.load(file)
        
#couchDB will not store big INTs, convert to string 

for tweet in data:
    if str(tweet['tweet id']) in db:
        continue
    for key in tweet.keys():
        if type(tweet[key]) == int:
            tweet[key] = str(tweet[key])



    db[tweet['tweet id']] = tweet


