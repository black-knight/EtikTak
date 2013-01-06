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

import traceback

from piston import handler as piston
from django.db import transaction

class ApiResult:
    RESULT_KEY = "result"
    DESCRIPTION_KEY = "description"
    RESULT_OK = "OK"
    RESULT_FAILURE = "FAILURE"

class RequestHandler(piston.BaseHandler):
    """
    An abstract transactional request handler inheriting from piston.handler.BaseHandler.

    Transactions are handled automatically and rollback hence performed if an error
    occurs.

    Moreover, if an exception is raised an error object along with its description will be
    returned (in the given request format). If there is no result given from the request
    method an OK result will be returned; else the result is directly returned.
    """
    allowed_methods = ('GET',)

    @transaction.commit_manually
    def read(self, request, *args, **kwargs):
        """
        Handles incoming request. Wraps self.get-method in transaction/error handling.
        """
        try:
            result = self.get(request, *args, **kwargs)
            transaction.commit()
            return self.ok(result)
        except BaseException as e:
            transaction.rollback()
            traceback.print_exc()
            return self.error(e.message)

    def get(self, request, *args, **kwargs):
        """
        Abstract method to implement. Is called by self.read and is thus wrapped in
        transaction/error handling.
        """
        raise NotImplementedError("Method not implemented")

    def ok(self, result=None):
        """
        Returns the given result, if any, or else a generic OK result.
        """
        if result is None:
            return {ApiResult.RESULT_KEY: ApiResult.RESULT_OK}
        else:
            return result

    def error(self, text=''):
        """
        Returns an error with the given error description.
        """
        return {ApiResult.RESULT_KEY: ApiResult.RESULT_FAILURE,
                ApiResult.DESCRIPTION_KEY: text}
