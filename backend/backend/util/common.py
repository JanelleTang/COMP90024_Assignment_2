import ujson
import datetime

from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.utils.dateparse import parse_datetime

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

def json_string_to_dict(keys, source):
    data = ujson.load(source)
    result = []
    for item in data["data"]:
        for key in keys:
            if key not in item:
                item[key] = ""
        result.append(item)
    return result