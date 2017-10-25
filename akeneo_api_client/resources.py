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

class CreatableResource(CreatableResourceInterface):
    def create_item(self, item):
        url = self._endpoint
        logger.debug(json.dumps(item, separators=(',', ':')))
        r = self._session.post(url, data=json.dumps(item, separators=(',', ':')))

        if r.status_code != 201:
            raise requests.HTTPError("Status code: {0}. Content: {1}".format(
                r.status_code,
                r.text))

class ListableResource(ListableResourceInterface):
    def fetch_list(self, **kwargs):
        """Send a request with search, etc.
        Returns an iterable list (Collection)"""
        url = self._endpoint
        r = self._session.get(url)

        if r.status_code != 200:
            raise requests.HTTPError("Status code: {0}".format(r.status_code))

        c = Collection(self._session, json_text=r.text)
        return c

class GettableResource(GettableResourceInterface):
    def fetch_item(self, code):
        """Returns a unique item object"""
        logger.debug(self._endpoint)
        url = urljoin(self._endpoint, code)
        logger.debug(url)
        r = self._session.get(url)

        if r.status_code != 200:
            raise requests.HTTPError("The item {0} doesn't exit".format(code))

        logger.debug(r.status_code)
        logger.debug(r.text)
        return json.loads(r.text) # returns item as a dict

class DeletableResource(DeletableResourceInterface):
    def delete_item(self, code):
        logger.debug(self._endpoint)
        url = urljoin(self._endpoint, code)
        r = self._session.delete(url)

        if r.status_code != 204:
            raise requests.HTTPError("The item {0} doesn't exit. Content: {1}".format(
                r.status_code,
                r.text))

class IdentifierBasedResource(CodeBasedResourceInterface):
    def get_code(self, item):
        return item['identifier']

class CodeBasedResource(CodeBasedResourceInterface):
    def get_code(self, item):
        return item['code']


class ResourcePool(
    CreatableResource,
    DeletableResource,
    GettableResource,
    ListableResource,):
    def __init__(self, endpoint, session):
        """Initialize the ResourcePool to the given endpoint. Eg: products"""
        self._endpoint = endpoint
        self._session = session
        pass
