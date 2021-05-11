import ujson
import logging
import time

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from backend.util.couchDBUtil import couch_db
from backend.util.common import *
logger = logging.getLogger('django.debug')


@require_http_methods(['POST'])
def create_raw_tweet(request):
    resp = None
    tweets = json_string_to_dict(['id', 'text', 'location', 'geo', 'hashtags'], request.body)
    if len(tweets) == 0:
        resp = ResponseMessage(404, "empty tweets", None)
        return resp.response()
    
    for tweet in tweets:
        tweet['_id'] = tweet['id']
        tweet.pop('id')
        tweet['isProcessed'] = 0
    
    try:
        twitter_db = couch_db.getDatabase("twitter")
        response_list = twitter_db.update(tweets)
        for success, docid, rev in response_list:
            if not success:
                resp = ResponseMessage(500, "saving tweets failed", None)
                return resp.response()
        resp = ResponseMessage(200, "success", None)
    except Exception as e:
        logger.info(e)
        resp = ResponseMessage(500, "saving tweets failed", None)

    return resp.response()

## TO DO
@require_http_methods(['POST'])
def update_raw_tweet(request, id=None):
    obj = {"success": True}
    return json_response(obj)

@require_http_methods(['GET'])
def delete_raw_tweet_by_id(request, id=None):
    obj = {"success": True}
    return json_response(obj)

@require_http_methods(['GET'])
def get_raw_tweet_by_size(request, size=1000):
    resp = None
    try:
        twitter_db = couch_db.getDatabase("twitter")
        tweets = twitter_db.view('tweet/get_raw', limit=size)
        
        tweet_data = dict()
        for row in tweets:
            tweet_data[row.id] = {
                "id": row.id,
                "text": row.value["text"],
                "geo": row.value["geo"],
                "location": row.value["location"],
                "hashtags": row.value["hashtags"],
            }

        resp = ResponseMessage(200, "success", tweet_data)
    except Exception as e:
        logger.error("Unable to get the raw tweet data")
        logger.error(e)
        resp = ResponseMessage(500, "fail", None)
    return resp.response()