import ujson
import datetime

from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.utils.dateparse import parse_datetime

def json_response(response):
    return HttpResponse(ujson.dumps(response), content_type='application/json')
