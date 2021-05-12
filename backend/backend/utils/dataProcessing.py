from couchdb import *
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .sentimentAnalysis import CleanTweet
from geopy.geocoders import Nominatim
import ujson
from .couchDButil import *
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest

geolocator = Nominatim(user_agent="tweets")

# db_server = CouchDBDriver
# raw_tweets_db = db_server["test"] ## CHANGE NAME
# try:
#     regions_db = db_server.create('regions') ## Remove if created
# except PreconditionFailed:
#     regions_db = db_server['regions']

def pull_tweets(db):
    for row in db:
        tweet_row = db[row] ## Remove this part - just extra IDs and levels 
        tweet = tweet_row['text']
        location = tweet_row['location']
        lga,state = get_lga(location)
        tweet_obj = CleanTweet(tweet)
        sentiment = tweet_obj.sentiment_value
        try:
            regions_db[lga] = {'name':lga,
                            'state':state,
                            'total_sentiment':sentiment,
                            'total_tweets':1}
        except ResourceConflict:
            doc = regions_db[lga]
            doc['total_sentiment'] = doc['total_sentiment']+sentiment
            doc['total_tweets'] = doc['total_tweets']+1
        
def get_lga(location):
    location = geolocator.geocode(location,addressdetails=True)
    address = location.raw['address']
    if address['country']!="Australia":
        print("Check this tweet location")
        return None,None,None
    if len(address) <3:
        return None,None,None
    return address["municipality"].lower(),address["state"].lower()   


@api_view(["GET","POST"])
def raw_tweets_api_view(request):
    if request.method =="GET":
        lim = 2
        return get_raw_tweets(request,lim)

@api_view(["GET","PUT"])
def regions_api_view(request,pk):
    try:
        regions_db[pk]
    except ResourceNotFound:
        return Response({"error": {
                            "code": 404,
                            "message": "Region not found."
                            }
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method =="GET":
        return get_region_detail(request,pk)

@api_view(["GET","POST"])
def regions_api_view(request,pk):
    if request.method == "POST":
        return create_regions_point(request)

def get_raw_tweets(request,lim):
    # If your database has a design document and view under the path 
    # /db_name/_design/design_doc/_view/view_name, 
    # you can iterate this view using this syntax:
    tweets = current_db.view('design_doc/view_name',lim)

    for row in tweets:
        response_dict = couch_to_dict('_id',['text','geo','location'],tweets[row])

    return json_response(response_dict)

def get_region_detail(request,pk):
    region = regions_db[pk]
    response_dict = couch_to_dict('lga',['name',
                                        'state',
                                        'total_sentiment',
                                        'total_tweets'],region)
    return json_response(response_dict)                                    

def create_regions_point(request):
    if request.body:
        data = ujson.loads(request.body)
    else:
        data = {}
    for row in data:
        try:
            regions_db[row['lga']] = {'name':data['name'],
                                    'state':data['state'],
                                    'total_sentiment':data['sentiment'],
                                    'total_tweets':1}
        except ResourceConflict:
            doc = regions_db[lga]
            doc['total_sentiment'] = doc['total_sentiment']+sentiment
            doc['total_tweets'] = doc['total_tweets']+1
            doc.save()
    return Response(data,status=status.HTTP_201_CREATED)

