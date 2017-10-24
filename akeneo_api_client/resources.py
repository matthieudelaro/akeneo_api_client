# -*- coding: utf-8 -*-

from akeneo_api_client.utils import *
from akeneo_api_client.interfaces import *
from akeneo_api_client.collection import *
import requests
import json

import logging
import logzero
from logzero import logger

import urllib.parse


class ResourcePool:
    def __init__(self, endpoint, session):
        """Initialize the ResourcePool to the given endpoint. Eg: products"""
        self._endpoint = endpoint
        self._session = session
        pass

    def fetch_list(self, **kwargs):
        """Send a request with search, etc.
        Returns an iterable list (Collection)"""
        url = self._endpoint
        r = self._session.get(url)

        if r.status_code != 200:
            raise requests.HTTPError("Status code: {0}".format(r.status_code))

        c = Collection(self._session, json_text=r.text)
        return c

    def fetch_item(self, id):
        """Returns a unique item object"""
        logger.debug(self._endpoint)
        url = urljoin(self._endpoint, id)
        logger.debug(url)
        r = self._session.get(url)

        if r.status_code != 200:
            raise requests.HTTPError("The item {0} doesn't exit".format(id))

        logger.debug(r.status_code)
        logger.debug(r.text)
        return json.loads(r.text) # returns item as a dict

