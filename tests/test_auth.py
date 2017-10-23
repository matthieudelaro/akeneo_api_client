# -*- coding: utf-8 -*-

from akeneo_api_client.auth import Auth

import requests
from requests.auth import AuthBase
from akeneo_api_client.utils import urljoin
import unittest
import base64
import json
from time import time

import logging
import logzero
from logzero import logger

from vcr_unittest import VCRTestCase


# class TestAuthIntegration(unittest.TestCase):
#     client_id = '1_ovvscbaj0pwwg8sookkgkc8ck4kog8gscg8g44sc88c8w48ww'
#     secret = 'rpi0wuiusa8okok4cw8kkkc4s488gc0sggkc0480wskkgkwo0'
#     username = 'admin'
#     password = 'admin'
#     base_url = 'http://localhost:8080'

    
#     def test_query_products_with_auth(self):
#         auth = Auth(self.base_url,
#             self.client_id, self.secret, self.username, self.password)
#         r = requests.get(urljoin(self.base_url, '/api/rest/v1/products?search={"enabled":[{"operator":"=","value":true}],"completeness":[{"operator":">","value":70,"scope":"ecommerce"}]}'), auth=auth)
#         logger.debug(r)
#         logger.debug(r.status_code)
#         json_data = json.loads(r.text)
#         logger.debug(json.dumps(json_data, indent=4, sort_keys=True))



class TestAuthIntegrationMock(VCRTestCase):
    client_id = '1_5hoodnvr69kwkw0cgkkwgwwoo8skwog4k8wsscgc0o0css8ggo'
    secret = '5k677icg34owogww0wocoows8g4004so40skk0s0s88g4ws8gg'
    username = 'admin'
    password = 'admin'
    base_url = 'http://localhost:8080'
    
    def _get_vcr(self, **kwargs):
        logzero.loglevel(logging.INFO)
        myvcr = super(TestAuthIntegrationMock, self)._get_vcr(**kwargs)
        myvcr.match_on = ['method', 'host', 'port', 'path', 'query', 'body', 'headers']
        myvcr.record_mode='none'
        return myvcr

    def test_valid(self):
        auth = Auth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        auth._request_a_token()
        auth._refresh_the_token()

    def test_invalid_request(self):
        auth = Auth(self.base_url,
            self.client_id, "fake secret", self.username, self.password)
        with self.assertRaises(requests.exceptions.HTTPError):
            auth._request_a_token()

    def test_invalid_refresh(self):
        auth = Auth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        auth._request_a_token()
        with self.assertRaises(requests.exceptions.HTTPError):
            auth._refresh_token = "coucou"
            auth._refresh_the_token()

    def test_should_refresh_request(self):
        auth = Auth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        auth._request_a_token()
        logger.debug(int(time()))
        logger.debug(auth._expiry_date)
        self.assertFalse(auth._should_refresh_token())
        auth._expiry_date = time() - 100
        self.assertTrue(auth._should_refresh_token())

    def test_query_products_with_auth(self):
        auth = Auth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        r = requests.get(urljoin(self.base_url, "/api/rest/v1/products"), auth=auth)
        logger.debug(r)
        logger.debug(r.status_code)
        json_data = json.loads(r.text)
        logger.debug(json.dumps(json_data, indent=4, sort_keys=True))


# or run with > python-api-client$ pipenv run nosetests
if __name__ == '__main__':
    logzero.loglevel(logging.INFO)
    unittest.main()

