import json
from django.contrib.gis.geos import GEOSGeometry
from locations.models import Region
from random import randint

with open('locations/analytics/data/regions_data.json', 'r') as f:
    data = json.load(f)
    val = [1,2,3,4,5]
    for area,properties in data.items():
        i = randint(0,4)
        LGA = Region(name=area,state=properties["state"],
            polygon=GEOSGeometry(json.dumps(properties["geometry"])),
            sentiment_value =properties["total_sentiment"], 
            sentiment_rank = val[i],
            n_tweets = properties["total_tweets"])
        LGA.save()
