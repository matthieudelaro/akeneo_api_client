# -*- coding: utf-8 -*-

from akeneo_api_client.utils import *
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

    def get_list(self, **kwargs):
        """Send a request with search, etc.
        Returns an iterable list (Collection)"""
        url = self._endpoint
        r = self._session.get(url)

        if r.status_code != 200:
            raise requests.HTTPError("Status code: {0}".format(r.status_code))

        c = Collection(self._session, json_text=r.text)
        return c

    def get_item(self, id):
        """Returns a unique item object"""
        logger.debug(self._endpoint)
        url = urljoin(self._endpoint, id)
        logger.debug(url)
        r = self._session.get(url)

        if r.status_code != 200:
            raise requests.HTTPError("The item {0} doesn't exit".format(id))

        logger.debug(r.status_code)
        logger.debug(r.text)
        # return json.loads(r.text) : returns a dict
        return json2object(r.text) # returns an object


class Collection:
    def __init__(self, session, json_data=None, json_text=None):
        if json_text and not json_data:
            json_data = json.loads(json_text)
        elif json_data and not json_text:
            # json_data = json_data
            pass
        else:
            raise ValueError("Please provide either json_data, or json_text.")
        if not session:
            raise ValueError("session should be provided")
        self._session = session
        logger.debug(json_data)
        self._link_first = json_data["_links"]["first"]
        self._link_next = urllib.parse.unquote(json_data["_links"]["next"]["href"])
        self._items = [json2object(json.dumps(item))
                       for item in json_data["_embedded"]["items"]]

    def get_list(self):
        return self._items

    def fetch_more_items(self):
        if not self._link_next:
            raise StopIteration()
        else:
            r = self._session.get(self._link_next)
            if r.status_code != 200:
                raise StopIteration()
            else:
                json_data = json.loads(r.text)
                self._link_next = urllib.parse.unquote(json_data["_links"]["next"]["href"])
                self._items += [json2object(json.dumps(item))
                       for item in json_data["_embedded"]["items"]]

    def __iter__(self):
        return CollectionIterator(self)


class CollectionIterator:
    def __init__(self, collection):
        self.i = 0
        self._collection = collection
        self.count = len(self._collection.get_list())

    def __iter__(self):
        # Iterators are iterables too.
        # Adding this functions to make them so.
        return self

    def __next__(self):
        if not self.i < self.count:
            self._collection.fetch_more_items()
            self.count = len(self._collection.get_list())

        if self.i < self.count:
            item = self._collection.get_list()[self.i]
            self.i += 1
            return item
        else:
            raise StopIteration()