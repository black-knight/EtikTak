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

from etiktak.api.user_handlers import *
from etiktak.api.product_handlers import *
from etiktak.api.sms_handlers import *

from django.conf.urls import *
from piston.resource import Resource

create_user_handler = Resource(ApplyUserHandler)
verify_user_handler = Resource(VerifyUserHandler)
scan_product_handler = Resource(ScanProductHandler)
sms_callback_handler = Resource(SmsCallbackHandler)

urlpatterns = patterns('',
    url(r'^users/apply/(?P<mobile_number>[^/]+)/(?P<password>[^/]+)/$', create_user_handler, { 'emitter_format' : 'json' }),
    url(r'^users/verify/(?P<mobile_number>[^/]+)/(?P<password>[^/]+)/(?P<sms_challenge>[^/]+)/(?P<client_challenge>[^/]+)/$', verify_user_handler, { 'emitter_format' : 'json' }),
    url(r'^products/scan/(?P<mobile_number>[^/]+)/(?P<password>[^/]+)/(?P<uid>[^/]+)/(?P<barcode>[^/]+)/(?P<barcode_type>[^/]+)/(?P<scan_latitude>[^/]+)/(?P<scan_longitude>[^/]+)/$', scan_product_handler, { 'emitter_format' : 'json' }),
    url(r'^sms/callback/$', sms_callback_handler, { 'emitter_format' : 'json' }),
)
