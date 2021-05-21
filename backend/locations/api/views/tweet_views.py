# ============================ TWITTER VIEW APIs ============================ #
#   
#
#
# ========================================================================== #

from backend.utils.common import *
from backend.utils.couchDButil import *
from django.views.decorators.http import require_http_methods
import logging
import ujson
from couchdb import *

logger = logging.getLogger('django.debug')


@require_http_methods(['POST'])
def create_raw_tweet(request):
    resp = None
    tweets = string_to_list_dict(['id', 'text', 'location', 'geo', 'hashtags','date_created'], request.body)
    if len(tweets) == 0:
        resp = ResponseMessage(404, "empty tweets", None)
        return resp.response()
    try:
        twitter_db = couch_db.getDatabase("twitter")
        
        for tweet in tweets:
            try:
                tweet['isProcessed'] = 0
                tweet_id = tweet['id']
                tweet.pop('id')
                twitter_db[tweet_id] = tweet
            except ResourceConflict:
                print("tweet {} is duplicate.".format(tweet_id))
        resp = ResponseMessage(200, "success", None)
    except Exception as e:
        logger.info(e)
        resp = ResponseMessage(500, "saving tweets failed:\n"+str(e), None)
    return resp.response()

@require_http_methods(['POST'])
def update_raw_tweet(request, pk=None):
    resp = None
    try:
        twitter_db = couch_db.getDatabase("twitter")
        doc = twitter_db[pk]
        ## TO FINISH ##



        resp = ResponseMessage(200, "Successfully deleted", doc)
    except Exception as e:
        logger.error("Unable to delete {} tweet data".format(pk))
        logger.error(e)
        resp = ResponseMessage(500, "Fail:\n"+str(e), None)
    return resp.response()

@require_http_methods(['GET'])
def delete_raw_tweet_by_id(request, pk=None):
    resp = None
    try:
        twitter_db = couch_db.getDatabase("twitter")
        doc = twitter_db[pk]
        twitter_db.delete(doc)
        resp = ResponseMessage(200, "Successfully deleted", doc)
    except Exception as e:
        logger.error("Unable to delete {} tweet data".format(pk))
        logger.error(e)
        resp = ResponseMessage(500, "Fail:\n"+str(e), None)
    return resp.response()

@require_http_methods(['GET'])
def get_raw_tweet_by_size(request, size=1000):
    resp = None
    try:
        twitter_db = couch_db.getDatabase("twitter")
        tweets = twitter_db.view('tweet/get_raw', limit=size)
        tweet_data = []
        for row in tweets:
            doc = twitter_db[row.id]
            doc['isProcessed'] = 1
            twitter_db.save(doc)
            tweet_data.append(couch_to_dict(row.id,['text','geo','location','hashtags','date_created'],row.value))
        resp = ResponseMessage(200, "success", tweet_data)
    except Exception as e:
        logger.error("Unable to get the raw tweet data")
        logger.error(e)
        resp = ResponseMessage(500, "fail:\n"+str(e), None)
    return resp.response()


@require_http_methods(['POST'])
def create_tweet_times(request):
    resp = None
    time_data = ujson.loads(request.body)['data']
    if len(time_data) == 0:
        resp = ResponseMessage(404, "empty time data", None)
        return resp.response()

    try:
        time_db = couch_db.getDatabase("times")
        for row in time_data:
            try:
                pk = row['city']+"__"+row['time']
                time_db[pk] = {'time':row['time'],'city':row['city'],'count':1}
            except ResourceConflict:
                doc = time_db[pk]
                doc['count'] = doc['count']+1
                time_db.save(doc)
        resp = ResponseMessage(200, "success", None)
    except Exception as e:
        logger.info(e)
        resp = ResponseMessage(500, "saving time data failed:\n"+str(e), None)
    return resp.response()

@require_http_methods(['POST'])
def create_tweet_dates(request):
    resp = None
    date_data = ujson.loads(request.body)['data']
    if len(date_data) == 0:
        resp = ResponseMessage(404, "empty date data", None)
        return resp.response()
    try:
        date_db = couch_db.getDatabase("dates")
        for row in date_data:
            try:
                pk = row['city']+"__"+row['date']
                date_db[pk] = {'id': pk,'date':row['date'],'city':row['city'],'count':1}
            except ResourceConflict:
                doc = date_db[pk]
                doc['count'] = doc['count']+1
                date_db.save(doc)
        resp = ResponseMessage(200, "success", None)
    except Exception as e:
        logger.info(e)
        resp = ResponseMessage(500, "saving date data failed:\n"+str(e), None)
    return resp.response()

@require_http_methods(['GET'])
def get_tweet_times(request,pk):
    resp = None
    try:
        times_db = couch_db.getDatabase("times")
        times = times_db.view('times/{}'.format(pk))
        times_data = []
        for time_string in times:
            doc = times_db[time_string]
            times_data.append(couch_to_dict(None,['time','city','count'],doc))

        resp = ResponseMessage(200, "success", times_data)
    except Exception as e:
        logger.error("Unable to get location data 1")
        logger.error(e)
        resp = ResponseMessage(500, "fail:\n"+str(e), None)
    return resp.response()

@require_http_methods(['GET'])
def get_tweet_dates(request,pk):
    resp = None
    try:
        dates_db = couch_db.getDatabase("dates")
        dates_view = dates_db.view('dates/get_all')
        print(dates_view)
        for date_string in dates_db:
            doc = dates_db[date_string]
            print(doc)
            if doc.city == pk.replace("_"," "):
                dates_data.append(couch_to_dict(None,['date','city','count'],doc))
        resp = ResponseMessage(200, "success", dates_data)
    except Exception as e:
        logger.error("Unable to get location data 1")
        logger.error(e)
        resp = ResponseMessage(500, "fail:\n"+str(e), None)
    return resp.response()