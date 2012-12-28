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

from etiktak.service import user_service
from etiktak.util import util

from piston.handler import BaseHandler

class ApplyUserHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, mobile_number=None, password=None):
        try:
            mobile_number = util.getRequiredParam(request, 'mobile_number')
            password = util.getRequiredParam(request, 'password')
            user_service.apply_for_user(mobile_number, password)
            return {"result": "OK"}
        except Exception as e:
            return {"result": e}

class VerifyUserHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, mobile_number=None, password=None, challenge=None):
        try:
            mobile_number = util.getRequiredParam(request, 'mobile_number')
            password = util.getRequiredParam(request, 'password')
            challenge = util.getRequiredParam(request, 'challenge')
            user_service.verify_user(mobile_number, password, challenge)
            return {"result": "OK"}
        except Exception as e:
            return {"result": e}
