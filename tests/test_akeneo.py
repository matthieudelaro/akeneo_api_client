# -*- coding: utf-8 -*-

from akeneo_api_client.collection import *
from akeneo_api_client.resources import *
from akeneo_api_client.auth import Auth
from akeneo_api_client.utils import urljoin
from akeneo_api_client.client import *

import requests
from requests.auth import AuthBase
import unittest
import base64
import json
from time import time

import logging
import logzero
from logzero import logger

from vcr_unittest import VCRTestCase

import copy


class TestClient(VCRTestCase):
    client_id = '1_ovvscbaj0pwwg8sookkgkc8ck4kog8gscg8g44sc88c8w48ww'
    secret = 'rpi0wuiusa8okok4cw8kkkc4s488gc0sggkc0480wskkgkwo0'
    username = 'admin'
    password = 'admin'
    base_url = 'http://localhost:8080'

    def _get_vcr(self, **kwargs):
        logzero.loglevel(logging.INFO)
        myvcr = super(TestClient, self)._get_vcr(**kwargs)
        myvcr.match_on = ['method', 'path', 'query', 'body', 'headers']
        myvcr.record_mode='none'
        return myvcr

    def test_association_types(self):
        akeneo = Client(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        item = akeneo.association_types.fetch_item('PACK')
        self.assertIsNotNone(item)

    def test_products(self):
        akeneo = Client(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        item = akeneo.products.fetch_item('1111111137')
        items = akeneo.products.fetch_list().get_list()
        self.assertIsNotNone(item)
        self.assertEquals(len(items), 10)

    def test_get_resources(self):
        akeneo = Client(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        for name in akeneo.RESOURCE_NAMES:
            pool = getattr(akeneo, name)
            items = pool.fetch_list().get_list()
            self.assertTrue(len(items) > 2)

    def test_client_auth_invalid(self):
        with self.assertRaises(ValueError):
            akeneo = Client(self.base_url, self.password)

    def test_client_auth_credential(self):
        akeneo = Client(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        item = akeneo.products.fetch_item('1111111137')

    def test_client_auth_object(self):
        auth=Auth(self.base_url, self.client_id, self.secret,
            self.username, self.password)
        akeneo = Client(self.base_url, session=None,
            auth=auth)
        item = akeneo.products.fetch_item('1111111137')

    valid_product = """{"identifier":"myawesometshirt","enabled":true,"family":"clothing","categories":["master_men_blazers"],"groups":[],"parent":null,"values":{"collection":[{"data":["summer_2017"],"locale":null,"scope":null}],"color":[{"data":"white","locale":null,"scope":null}],"description":[{"data":"Biker jacket","locale":"en_US","scope":"ecommerce"}],"ean":[{"data":"1234567946367","locale":null,"scope":null}],"material":[{"data":"polyester","locale":null,"scope":null}],"name":[{"data":"Biker jacket","locale":null,"scope":null}],"price":[{"data":[{"amount":null,"currency":"EUR"},{"amount":null,"currency":"USD"}],"locale":null,"scope":null}],"size":[{"data":"xl","locale":null,"scope":null}],"variation_name":[{"data":"Biker jacket polyester","locale":"en_US","scope":null}]}}"""

    