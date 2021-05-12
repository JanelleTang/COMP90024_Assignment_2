from backend.utils.common import *
from backend.utils.couchDButil import *
from django.views.decorators.http import require_http_methods
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

        for row in tweets:
            tweet_data = couch_to_dict(row.id,['text','geo','location','hashtags'],row.value)

        resp = ResponseMessage(200, "success", tweet_data)
    except Exception as e:
        logger.error("Unable to get the raw tweet data")
        logger.error(e)
        resp = ResponseMessage(500, "fail", None)
    return resp.response()



# ============================ REGION VIEW APIs ============================ #
@require_http_methods(['POST'])
def create_region(request):
    resp = None
    regions = string_to_list_dict(['id', 'state', 'total_sentiment', 'sentiment'], request.body)
    if len(tweets) == 0:
        resp = ResponseMessage(404, "empty regions", None)
        return resp.response()

    try:
        regions_db = couch_db.getDatabase("regions")
        for row in regions:
            try:
                regions_db[row['id']] = {'state':row['state'],
                                        'total_sentiment':row['sentiment'],
                                        'total_tweets':1}
            except ResourceConflict:
                doc = regions_db[row['id']]
                doc['total_sentiment'] = doc['total_sentiment']+row['sentiment']
                doc['total_tweets'] = doc['total_tweets']+1
                doc.save()

        response_list = regions_db.update(regions)
        for success, docid, rev in response_list:
            if not success:
                resp = ResponseMessage(500, "saving regions failed", None)
                return resp.response()
        resp = ResponseMessage(200, "success", None)
    except Exception as e:
        logger.info(e)
        resp = ResponseMessage(500, "saving regions failed", None)

    return resp.response()

@require_http_methods(["GET","POST"])
def regions_api_view(request,pk):
    if request.method == "POST":
        return create_regions_point(request)

@require_http_methods(['GET'])
def get_region(request):
    resp = None
    regions = string_to_list_dict(['id', 'state', 'total_sentiment', 'sentiment'], request.body)
    if len(tweets) == 0:
        resp = ResponseMessage(404, "empty regions", None)
        return resp.response()

    try:
        regions_db = couch_db.getDatabase("regions")
        for row in regions:
            try:
                regions_db[row['id']] = {'state':row['state'],
                                        'total_sentiment':row['sentiment'],
                                        'total_tweets':1}
            except ResourceConflict:
                doc = regions_db[row['id']]
                doc['total_sentiment'] = doc['total_sentiment']+row['sentiment']
                doc['total_tweets'] = doc['total_tweets']+1
                doc.save()

        response_list = regions_db.update(regions)
        for success, docid, rev in response_list:
            if not success:
                resp = ResponseMessage(500, "saving regions failed", None)
                return resp.response()
        resp = ResponseMessage(200, "success", None)
    except Exception as e:
        logger.info(e)
        resp = ResponseMessage(500, "saving regions failed", None)

    return resp.response()


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

