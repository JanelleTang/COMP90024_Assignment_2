# # from django.shortcuts import render
# from numpy.lib.function_base import average
import requests
import pandas as pd
import django 
from django.contrib.gis.geos import GEOSGeometry
import json
from django.core.exceptions import ObjectDoesNotExist
import django
import os
import logging
from django.views.decorators.http import require_http_methods
from .models import LGA,City
from time import sleep
from backend.utils.common import *



@require_http_methods(['GET'])
def update_city_instances(requests):
    path = 'http://172.26.134.122/api/location/city'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()

    city_dict = {
        'melbourne':'POINT(144.9631 -37.8136)',
        'sydney':'POINT(151.2093 -33.8688)',
        'brisbane city':'POINT(153.0260 -27.4705)',
        'adelaide':'POINT(138.6007 -34.9285)',
        'perth': 'POINT(115.8613 -31.9523)',
        'hobart': 'POINT(147.3257 -42.8826)',
        'ballarat': 'POINT(143.8503 -37.5622)',
        'cairns':'POINT(145.7710 -16.9203)',
        'newcastle': 'POINT(151.7817 -32.9283)'
    }
    try:
        CouchToInstances(path,city_dict,True)
        print("Cities updated.")
        
    except Exception as e:
        logger.info(e)
        resp = ResponseMessage(500, "Updating model instances failed. Try Again.", None)
    resp = ResponseMessage(200, "success", None)
    return resp.response()

def update_lga_instances(requests):
    path = 'http://172.26.134.122/api/location/lga'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()

    with open('locations/data/shapefiles/combined_lga_data.json') as f:
        lga_dict = json.load(f)

    try:
        CouchToInstances(path,lga_dict,False)
        print("LGAs updated.")
        
    except Exception as e:
        logger.info(e)
        resp = ResponseMessage(500, "Updating model instances failed. Try Again.", None)
    resp = ResponseMessage(200, "success", None)
    return resp.response()


## ========================== Region Polygons ========================== #
def CouchToInstances(path,geo_dict,isCity):
    region_data = requests.get(path).json()['obj']
    update_model_data(region_data,geo_dict,isCity)

def update_model_data(data,geom_dict,is_city=True):
    for row in data:
        for k,v in row.items():
            try:
                update_instance(v,geom_dict,is_city)
            except:
                print('Something wrong with uploading: ',v)

## create model instances here
def update_instance(data,geom_dict,is_city):
    pk = data['name']
    if is_city:
        model=City
    else:
        model=LGA
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
        if is_city:
            obj = model(name = pk,
                    state = data['state'],
                    display_name = pk.title(),
                    polygon = geom,
                    sentiment_value = round(data['total_sentiment'],4),
                    sentiment_rank = sent_rank,
                    n_tweets = data['total_tweets'])
        else:
            obj = model(name = pk,
                display_name = pk.title(),
                state = data['state'],
                city = data['city'],
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