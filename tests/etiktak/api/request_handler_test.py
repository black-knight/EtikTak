import unittest

from etiktak.api import request_handler
from etiktak.api.request_handler import ApiResult
from etiktak.model.clients import models as clients

class RequestHandlerTest(unittest.TestCase):
    def will_rollback_transaction_on_exception_test(self):
        (TEST_MOBILE_NUMBER, TEST_PASSWORD) = ("12345678", "test1234")
        result = RollbackTransactionTestHandler().read(None, mobile_number=TEST_MOBILE_NUMBER, password=TEST_PASSWORD)
        self.assertEquals(ApiResult.RESULT_FAILURE, result.get(ApiResult.RESULT_KEY), msg="Expected error from webservice")
        self.assertRaises(BaseException, clients.Client.objects.get, TEST_MOBILE_NUMBER, TEST_PASSWORD)

    def will_commit_transaction_on_success_test(self):
        (TEST_MOBILE_NUMBER, TEST_PASSWORD) = ("13243546", "test1234")
        client = CommitTransactionTestHandler().read(None, mobile_number=TEST_MOBILE_NUMBER, password=TEST_PASSWORD)
        self.assertIsInstance(client, clients.Client, "Expected client datatype from webservice")
        self.assertEqual(client, clients.Client.objects.get(TEST_MOBILE_NUMBER, TEST_PASSWORD))

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
