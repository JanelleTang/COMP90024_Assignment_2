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

@require_http_methods(['POST', 'GET'])
def tweet_test_point(request, *args, **kwargs):
    obj = {"success": True}
    return json_response(obj)