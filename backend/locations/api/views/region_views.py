# ============================ REGION VIEW APIs ============================ #
#   
#
#
# ========================================================================== #

from backend.utils.common import *
from backend.utils.couchDButil import *
from django.views.decorators.http import require_http_methods
import logging
from couchdb import *

@require_http_methods(['POST'])
def create_region(request):
    resp = None
    regions = ujson.loads(request.body)['data']
    #regions = string_to_list_dict(['lga', 'city', 'state', 'total_sentiment', 'total_tweets'], request.body)
    if len(regions) == 0:
        resp = ResponseMessage(404, "empty regions", None)
        return resp.response()
    try:
        regions_db = couch_db.getDatabase("regions")
        for row in regions:
            try:
                lga_id = row['lga'].replace(" ","-")
                regions_db[lga_id] = row
            except ResourceConflict:
                doc = regions_db[lga_id]
                doc['total_sentiment'] = doc['total_sentiment']+row['total_sentiment']
                doc['total_tweets'] = doc['total_tweets']+1
                regions_db.save(doc)
        resp = ResponseMessage(200, "success", None)
    except Exception as e:
        logger.info(e)
        resp = ResponseMessage(500, "saving regions2 failed", None)
    return resp.response()


@require_http_methods(['GET'])
def get_region(request):
    resp = None
    try:
        regions_db = couch_db.getDatabase("regions")
        regions_data = []
        for region_name in regions_db:
            print('log1')
            doc = regions_db[region_name]
            print('log2')
            regions_data.append(couch_to_dict(region_name,['lga','city','state', 'total_sentiment', 'total_tweets'],doc))
            print('log3')
        resp = ResponseMessage(200, "success", regions_data)
    except Exception as e:
        logger.error("Unable to get location data 1")
        logger.error(e)
        resp = ResponseMessage(500, "fail", None)
    return resp.response()


@require_http_methods(['GET'])
def get_region_detail(request,pk):

    resp = None
    try:
        regions_db = couch_db.getDatabase("regions")
        data = couch_to_dict(pk,['state', 'total_sentiment', 'total_tweets'],regions_db[pk])
        resp = ResponseMessage(200, "Success", data)
    except Exception as e:
        logger.error("Unable to get {} data".format(pk))
        logger.error(e)
        resp = ResponseMessage(500, "Fail", None)
    return resp.response()

@require_http_methods(['DELETE'])    
def delete_lga_detail(request,pk):    
    resp = None
    try:
        regions_db = couch_db.getDatabase("regions")
        doc = regions_db[pk]
        regions_db.delete(doc)
        resp = ResponseMessage(200, "Successfully deleted", doc)
    except Exception as e:
        logger.error("Unable to delete {} data".format(pk))
        logger.error(e)
        resp = ResponseMessage(500, "Fail", None)
    return resp.response()
