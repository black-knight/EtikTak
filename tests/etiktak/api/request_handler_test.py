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

import unittest

from etiktak.api import request_handler
from etiktak.api.request_handler import ApiResult
from etiktak.model.clients import models as clients

class RequestHandlerTest(unittest.TestCase):
    def will_rollback_transaction_on_exception_test(self):
        (TEST_MOBILE_NUMBER, TEST_PASSWORD) = ("12345678", "test1234")
        result = RollbackTransactionTestHandler().read(None, mobile_number=TEST_MOBILE_NUMBER, password=TEST_PASSWORD)
        self.assertEquals(ApiResult.RESULT_FAILURE, result.get(ApiResult.RESULT_KEY), msg="Expected error from webservice")
        self.assertRaises(BaseException, clients.Client.objects.get_by_password, TEST_MOBILE_NUMBER, TEST_PASSWORD)

    def will_commit_transaction_on_success_test(self):
        (TEST_MOBILE_NUMBER, TEST_PASSWORD) = ("13243546", "test1234")
        client = CommitTransactionTestHandler().read(None, mobile_number=TEST_MOBILE_NUMBER, password=TEST_PASSWORD)
        self.assertIsInstance(client, clients.Client, "Expected client datatype from webservice")
        self.assertEqual(client, clients.Client.objects.get_by_password(TEST_MOBILE_NUMBER, TEST_PASSWORD))

    def will_return_OK_when_no_result_supplied_test(self):
        result = NoResultTestHandler().read(None, None, None)
        self.assertEquals(ApiResult.RESULT_OK, result.get(ApiResult.RESULT_KEY))

    def will_return_correct_error_description_test(self):
        TEST_ERROR_DESC = "'Tis but a scratch!"
        result = ErrorDescriptionTestHandler().read(None, error=TEST_ERROR_DESC)
        self.assertEquals(TEST_ERROR_DESC, result.get(ApiResult.DESCRIPTION_KEY))



class RollbackTransactionTestHandler(request_handler.RequestHandler):
    def get(self, request, mobile_number="12345678", password="test1234"):
        clients.Client.create_client_key(mobile_number, password)
        raise ValueError("This exception should roll back transaction")

class CommitTransactionTestHandler(request_handler.RequestHandler):
    def get(self, request, mobile_number="12345678", password="test1234"):
        return clients.Client.create_client_key(mobile_number, password)

class NoResultTestHandler(request_handler.RequestHandler):
    def get(self, request, *args, **kwargs):
        pass

class ErrorDescriptionTestHandler(request_handler.RequestHandler):
    def get(self, request, error="ERROR", **kwargs):
        raise ValueError(error)
