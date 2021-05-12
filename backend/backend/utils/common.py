import ujson
import datetime

from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.utils.dateparse import parse_datetime


def json_response(d):
    return HttpResponse(ujson.dumps(d), content_type='application/json')

def couch_to_dict(doc_id, keys,doc):
    d = {}
    for k in keys:
        d[k] = doc[k]
    return {doc_id:d}


class ResponseMessage:
    def __init__(self, code=200, message="", obj=None):
        self.code = code
        self.message = message
        self.obj = obj

    def response(self):
        obj = {
            "code": self.code,
            "message": self.message,
            "obj": self.obj
        }
        return HttpResponse(ujson.dumps(obj), content_type='application/json')

def string_to_list_dict(keys, source):
    # Changed name to represent output
    data = ujson.loads(source)
    result = []
    for row in data["data"]:
        for key in keys:
            if key not in row:
                row[key] = ""
        result.append(row)
    return result