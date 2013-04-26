# encoding: utf-8

# Copyright (c) 2012, Daniel Andersen (dani_ande@yahoo.dk)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import urllib2
import simplejson as json
from lettuce.django import django_url
from lettuce import world
from django.test.client import Client

from etiktak.api.request_handler import ApiResult

APPLY_USER = "users/apply"
VERIFY_USER = "users/verify"
CREATE_PRODUCT_LOCATION_URL = "products/scan_location"
SMS_CALLBACK_URL = "sms/callback"

class WebserviceException(BaseException):
    def __init__(self, message):
        BaseException.__init__(self, message)

def verify_json_result(json, expected):
    if not json.get("result") == expected:
        raise WebserviceException("Unexpected result from webservice: %s" % json)

def parse_url(url, params = None):
    if params is None:
        return url
    url += "/"
    if isinstance(params, basestring):
        return url + params
    else:
        for param in params:
            url += urllib2.quote(param) + "/"
        return url

def call(url, params=None):
    try:
        url = parse_url(url, params)
        world.client = Client()
        world.response = world.client.get(django_url("/api/%s" % url), follow=True)
    except BaseException as e:
        raise WebserviceException(e)

def apply_for_user(mobile_number, password):
    call(APPLY_USER, [mobile_number, password])
    result = json.loads(world.response.content)
    verify_json_result(result, ApiResult.RESULT_OK)
    return result

def verify_user(mobile_number, password, challenge):
    call(VERIFY_USER, [mobile_number, password, challenge])
    result = json.loads(world.response.content)
    verify_json_result(result, ApiResult.RESULT_OK)
    return result["uid"]

def create_product_location(mobile_number, password, uid, barcode, barcode_type, geo_location):
    call(CREATE_PRODUCT_LOCATION_URL, [mobile_number, password, uid, barcode, barcode_type, geo_location])
    result = json.loads(world.response.content)
    verify_json_result(result, ApiResult.RESULT_OK)
    return result

def simulate_SMS_sent(mobile_number, sms_handle):
    call(SMS_CALLBACK_URL, "?sms_handle=" + urllib2.quote(sms_handle) + "&status=1&receiver=" + urllib2.quote(mobile_number))
    result = json.loads(world.response.content)
    verify_json_result(result, ApiResult.RESULT_OK)
    return result
