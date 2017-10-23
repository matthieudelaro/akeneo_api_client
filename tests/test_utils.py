# -*- coding: utf-8 -*-

import akeneo_api_client
import akeneo_api_client.utils
from akeneo_api_client.utils import *

import requests
import unittest
import base64
import json
from time import time

import logging
import logzero
from logzero import logger

from vcr_unittest import VCRTestCase


class TestUtils(unittest.TestCase):
    def setUp(self):
        logzero.loglevel(logging.DEBUG)
    
    def test_urljoin(self):
        self.assertEqual(
            akeneo_api_client.utils.urljoin('http://a.com/', 'b/', 'c/', 'd'),
            'http://a.com/b/c/d'
        )
        self.assertEqual(
            akeneo_api_client.utils.urljoin('http://a.com/', 'b//', 'c//', 'd'),
            'http://a.com/b/c/d'
        )
        self.assertEqual(
            akeneo_api_client.utils.urljoin('http://a.com/', 'b', 'c', 'd'),
            'http://a.com/b/c/d'
        )
        self.assertEqual(
            akeneo_api_client.utils.urljoin('http://a.com/', '/b/', 'c', 'd'),
            'http://a.com/b/c/d'
        )
