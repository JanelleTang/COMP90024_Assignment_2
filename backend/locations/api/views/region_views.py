# ============= COMP90024 - Assignment 2 ============= #
#                               
# The University of Melbourne           
# Team 37
#
# ** Authors: **
# 
# JJ Burke              1048105
# Janelle Tang          694209
# Shuang Qiu            980433
# Declan Baird-Watson   640975
# Avinash Rao           1024577 
# 
# Location: Melbourne
# ==================================================== 

from backend.utils.common import *
from backend.utils.couchDButil import *
from django.views.decorators.http import require_http_methods
import logging
from couchdb import *

@require_http_methods(['POST'])
def create_region(request):
    resp = None
    regions = ujson.loads(request.body)['data']
    if len(regions) == 0:
        resp = ResponseMessage(404, "empty regions", None)
        print('No new tweets')
        return resp.response()
    try:
        regions_db = couch_db.getDatabase("regions")
        for row in regions:
            try:
                city_id = row['city'].replace(" ","-")
                
                regions_db[city_id] = {'LGA':{row['lga']:row['aggregate_data']},
                                        'name':row['city'],
                                        'state':row['state'],
                                        'dates':{row['date']:row['aggregate_data']},
                                        'times':{row['time']:row['aggregate_data']},
                                        'hashtags':row['hashtags'],
                                        'total_sentiment':row['aggregate_data']['total_sentiment'],
                                        'total_tweets':1}
            except ResourceConflict:
                doc = regions_db[city_id]
                lga_id = row['lga']
                
                #update existing LGA
                if lga_id in doc['LGA']:
                    update_aggregate_data(doc['LGA'][lga_id],row['aggregate_data'])
                else:
                    doc['LGA'][lga_id]=row['aggregate_data']

                # update hashtags
                doc['hashtags'] = {tag: doc['hashtags'].get(tag, 0) + row['hashtags'].get(tag, 0) for tag in set(doc['hashtags']) | set(row['hashtags'])}
                # update existing date
                current_date = row['date']
                if current_date in doc['dates']:
                    update_aggregate_data(doc['dates'][current_date],row['aggregate_data'])
                else:
                    doc['dates'][current_date]=row['aggregate_data']
                #update existing time
                current_time = row['time']  
                if current_time in doc['times']:
                    update_aggregate_data(doc['times'][current_time],row['aggregate_data'])
                else:
                    doc['times'][current_time]=row['aggregate_data']
                update_aggregate_data(doc,row['aggregate_data'])
                regions_db.save(doc)

        resp = ResponseMessage(200, "success", None)
    except Exception as e:
        logger.info(e)
        resp = ResponseMessage(500, "saving regions2 failed", None)
    return resp.response()


@require_http_methods(['GET'])
def get_cities(request):
    resp = None
    try:
        regions_db = couch_db.getDatabase("regions")
        city_data = []
        for city_id in regions_db:
            doc = regions_db[city_id]
            city_data.append(couch_to_dict(city_id,['name','state','total_sentiment', 'total_tweets'],doc))
        resp = ResponseMessage(200, "success", city_data)
    except Exception as e:
        logger.error("Unable to get location data 1")
        logger.error(e)
        resp = ResponseMessage(500, "fail", None)
    return resp.response()

@require_http_methods(['GET'])
def get_lgas(request):
    resp = None
    try:
        regions_db = couch_db.getDatabase("regions")
        lga_data = []
        for city_id in regions_db:
            doc = regions_db[city_id]
            state_name = doc['state']
            for lga_id,lga_row in doc['LGA'].items():
                aggregate_data = lga_row
                aggregate_data['state'] = state_name
                aggregate_data['city'] = city_id.replace(" ","-")
                aggregate_data['name'] = lga_id
                lga_data.append({lga_id.replace(" ","-"):aggregate_data})
        resp = ResponseMessage(200, "success", lga_data)
    except Exception as e:
        logger.error("Unable to get location data 1")
        logger.error(e)
        resp = ResponseMessage(500, "fail", None)
    return resp.response()

@require_http_methods(['GET'])
def get_city_detail(request,pk):

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
def delete_city_detail(request,pk):    
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

@require_http_methods(['GET'])
def get_all_dates(request):
    resp = None
    dates_data = []
    try:
        regions_db = couch_db.getDatabase("regions")
        for city_id in regions_db:
            doc = regions_db[city_id]
            dates_data.append(couch_to_dict(None,['name','dates'],doc))
                
        resp = ResponseMessage(200, "Success", dates_data)
    except Exception as e:
        logger.error(e)
        resp = ResponseMessage(500, "Fail", None)
    return resp.response()

@require_http_methods(['GET'])
def get_all_times(request):
    resp = None
    times_data = []
    try:
        regions_db = couch_db.getDatabase("regions")
        for city_id in regions_db:
            doc = regions_db[city_id]
            times_data.append(couch_to_dict(None,['name','times'],doc))
                
        resp = ResponseMessage(200, "Success", times_data)
    except Exception as e:
        logger.error(e)
        resp = ResponseMessage(500, "Fail", None)
    return resp.response()

@require_http_methods(['GET'])
def get_city_dates(request,pk):
    resp = None
    pk = 'none_'+pk
    try:
        regions_db = couch_db.getDatabase("regions")
        data = couch_to_dict(None,['dates'],regions_db[pk])
        resp = ResponseMessage(200, "Success", data['dates'])
    except Exception as e:
        logger.error("Unable to get {} data".format(pk))
        logger.error(e)
        resp = ResponseMessage(500, "Fail", None)
    return resp.response()

@require_http_methods(['GET'])
def get_city_times(request,pk):
    resp = None
    pk = 'none_'+pk
    try:
        regions_db = couch_db.getDatabase("regions")
        data = couch_to_dict(None,['times'],regions_db[pk])
        resp = ResponseMessage(200, "Success", data['times'])
    except Exception as e:
        logger.error("Unable to get {} data".format(pk))
        logger.error(e)
        resp = ResponseMessage(500, "Fail", None)
    return resp.response()