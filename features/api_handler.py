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

import simplejson as json
from lettuce.django import django_url
from lettuce import world
from django.test.client import Client

APPLY_USER_URL = "users/apply"
VERIFY_USER_URL = "users/verify"

def parse_url(url, params = None):
    if params is None:
        return url
    first = True
    for (key, value) in params:
        url += "?" if first else "&"
        url += key + "=" + value
        first = False
    return url

def call(url, params = None):
    url = parse_url(url, params)
    world.client = Client()
    world.response = world.client.get(django_url("/api/%s" % url), follow=True)

def apply_for_user(mobile_number, password):
    call(APPLY_USER_URL, [("mobile_number", mobile_number), ("password", password)])
    result = json.loads(world.response.content)
    if not result.get("result") == "OK":
        raise BaseException("Could not apply for user: %s" % result)
    return result


def verify_user(mobile_number, challenge):
    call(VERIFY_USER_URL, [("mobile_number", mobile_number), ("challenge", challenge)])
