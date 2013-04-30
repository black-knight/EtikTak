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

import math

def getRequiredParam(request, param):
    value = request.GET.get(param)
    assert value is not None, "Missing request parameter: %s'" % param
    return value

def enum(**enums):
    return type('Enum', (), enums)

def cachedClassMethod(dictionary):
    def cached_decorator(f):
        def check_cache(cls, key):
            if key in dictionary:
                return dictionary[key]
            dictionary[key] = f(cls, key)
            return dictionary[key]
        return check_cache
    return cached_decorator

def meters_to_latitude(meters):
    return meters / 111111.0

def meters_to_longitude(meters, latitude):
    return meters / (111111.0 * math.cos(latitude * math.pi / 180.0))

def meters_to_aprox_longitude(meters):
    return meters_to_longitude(meters, 56.0)

def latitude_to_meters(latitude):
    return latitude * 111111

def longitude_to_meters(longitude, latitude):
    return longitude * 111111 * math.cos(latitude * math.pi / 180.0)
