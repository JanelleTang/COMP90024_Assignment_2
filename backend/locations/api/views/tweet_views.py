# ============================ TWITTER VIEW APIs ============================ #
#   
#
#
# ========================================================================== #

from backend.utils.common import *
from backend.utils.couchDButil import *
from django.views.decorators.http import require_http_methods
import logging
from couchdb import *

logger = logging.getLogger('django.debug')


@require_http_methods(['POST'])
def create_raw_tweet(request):
    resp = None
    tweets = string_to_list_dict(['id', 'text', 'location', 'geo', 'hashtags'], request.body)
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
                print("duplicate")
                resp = ResponseMessage(500, "saving tweets failed", None)
                return resp.response()
        resp = ResponseMessage(200, "success", None)
    except Exception as e:
        logger.info(e)
        resp = ResponseMessage(500, "saving tweets failed", None)
    return resp.response()

@require_http_methods(['POST'])
def update_raw_tweet(request, pk=None):
    resp = None
    try:
        twitter_db = couch_db.getDatabase("twitter")
        doc = twitter_db[pk]
        twitter_db.delete(doc)
        resp = ResponseMessage(200, "Successfully deleted", doc)
    except Exception as e:
        logger.error("Unable to delete {} tweet data".format(pk))
        logger.error(e)
        resp = ResponseMessage(500, "Fail", None)
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
        resp = ResponseMessage(500, "Fail", None)
    return resp.response()

@require_http_methods(['GET'])
def get_raw_tweet_by_size(request, size=1000):
    resp = None
    try:
        twitter_db = couch_db.getDatabase("twitter")
        tweets = twitter_db.view('tweet/get_raw', limit=size)
        tweet_data = []
        for row in tweets:
            tweet_data.append(couch_to_dict(row.id,['text','geo','location','hashtags'],row.value))
        resp = ResponseMessage(200, "success", tweet_data)
    except Exception as e:
        logger.error("Unable to get the raw tweet data")
        logger.error(e)
        resp = ResponseMessage(500, "fail", None)
    return resp.response()



