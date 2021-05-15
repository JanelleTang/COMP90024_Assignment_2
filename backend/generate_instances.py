
from numpy.lib.function_base import average
import requests
import pandas as pd
import django 
from django.contrib.gis.geos import GEOSGeometry
import json
from django.core.exceptions import ObjectDoesNotExist
import django
import os


## ========================== Region Polygons ========================== #

class CouchToInstances:
    def __init__(self,path,geo_dict,model):
        self.URL = 'http://127.0.0.1:8000/api/location/'
        self.region_data = requests.get(self.URL+path).json()['obj']
        update_model_data(self.region_data,geo_dict,model)


def dict_to_df(data):
    results = []
    for row in data:
        for k,v in row.items():
            results.append(v)

    df = pd.DataFrame(results)
    return df

def update_model_data(data,geom_dict,model):
    for row in data:
        for k,v in row.items():
            try:
                update_instance(v,geom_dict,model)
            except:
                print('Something wrong with uploading: ',v)



## create model instances here
def update_instance(data,geom_dict,model):
    pk = data['name']
    try:
        obj = model.objects.get(name=pk)
        obj.sentiment_rank = get_sentiment_rank(data['total_sentiment'],data['total_tweets'])
        obj.sentiment_value = round(data['total_sentiment'],4)
        obj.n_tweets = data['total_tweets']

    except ObjectDoesNotExist:
        try:
            geom = convert_to_geom(geom_dict[pk])
        except KeyError:
            print(pk+" does not exist in geojson")
            return None
        sent_rank = get_sentiment_rank(data['total_sentiment'],data['total_tweets'])
        obj = model(name = pk,
        state = data['state'],
        polygon = geom,
        sentiment_value = round(data['total_sentiment'],4),
        sentiment_rank = sent_rank,
        n_tweets = data['total_tweets'])

    obj.save()


def convert_to_geom(obj):
    if type(obj) == str:
        return GEOSGeometry(obj)
    coordinates = obj['geometry']
    return GEOSGeometry(json.dumps(coordinates))

def get_sentiment_rank(sentiment,count):
    average_sent = sentiment/count
    if average_sent <-0.66:
        return -3
    elif average_sent <-0.33:
        return -2
    elif average_sent <0:
        return -1
    elif average_sent == 0:
        return 0
    elif average_sent <=0.33:
        return 1
    elif average_sent <=0.66:
        return 2
    elif average_sent <=1:
        return 3



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from locations.models import LGA,City
with open('locations/data/shapefiles/combined_lga_data.json') as f:
    lga_dict = json.load(f)

city_dict = {
    'melbourne':'POINT(144.9631 -37.8136)',
    'sydney':'POINT(151.2093 -33.8688)',
    'brisbane city':'POINT(153.0260 -27.4705)',
    'adelaide':'POINT(138.6007 -34.9285)',
    'perth': 'POINT(115.8613 -31.9523)',
    'hobart': 'POINT(147.3257 -42.8826)',
}

CouchToInstances("city",city_dict,City)
CouchToInstances("lga",lga_dict,LGA)
    
