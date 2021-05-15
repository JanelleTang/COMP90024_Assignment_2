import json

import pandas as pd
import couchdb

with open("aurin.json") as f:
    data = json.load(f)



couch=couchdb.Server('http://admin:password@localhost:5984/')

db = couch['aurin_data']

for key,item in data.items():
    print(key)
    print(item)
    db[key] = item

