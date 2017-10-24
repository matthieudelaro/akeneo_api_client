# -*- coding: utf-8 -*-

from akeneo_api_client.utils import *
from akeneo_api_client.interfaces import *
import requests
import json

import logging
import logzero
from logzero import logger

import urllib.parse


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
        self._items = []
        self._parse_page(json_data)

    def get_list(self):
        return self._items

    def fetch_next_page(self):
        if not self._link_next:
            raise StopIteration()
        else:
            r = self._session.get(self._link_next)
            if r.status_code != 200:
                raise StopIteration()
            else:
                json_data = json.loads(r.text)
                self._parse_page(json_data)

    def _parse_page(self, json_data):
        next_link = json_data["_links"].get('next')
        if next_link:
            self._link_next = urllib.parse.unquote(next_link['href'])
        else:
            self._link_next = None
        self._items += json_data["_embedded"]["items"]

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
        # TODO: Improve performance by using an iterator on the list?
        if not self.i < self.count:
            self._collection.fetch_next_page()
            self.count = len(self._collection.get_list())

        if self.i < self.count:
            item = self._collection.get_list()[self.i]
            self.i += 1
            return item
        else:
            raise StopIteration()


class CollectionGenerator:
    """TODO: make a collection iterable as a generator instead of an iterator,
    to address performance concerns when handling a huge amount of data.
    See http://anandology.com/python-practice-book/iterators.html#generators."""
    pass