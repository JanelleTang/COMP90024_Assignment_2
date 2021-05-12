
import requests
import pandas as pd

path = "http://127.0.0.1:8000/api/location"
region_data = requests.get(path).json()['obj']

data = []
for row in region_data:
    for k,v in row.items():
        data.append(v)
df = pd.DataFrame(data)
city_data = df.groupby(['city','state'],as_index=False)['total_sentiment','total_tweets'].agg('sum').to_dict('index')
lga_data = df[~df.lga.astype(str).str.startswith('none_')]


## create model instances here


