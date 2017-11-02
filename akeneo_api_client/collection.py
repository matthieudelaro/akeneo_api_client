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
    """Holds the result of a search. It can be iterated through as a list,
    as an iterator, or as a generator. Note that only one iteration should be
    used on a given Collection object.
    Search results are paginated: https://api.akeneo.com/documentation/pagination.html

    Using Collection.get_iterator(), the next page will be loaded once the user
    iterated over the whole current page. The content of the new page will be
    appended at the end of the current list of items.

    Using Collection.get_generator(), the next page will be loaded once the user
    iterated over the whole current page. But items of previous pages will
    be forgotten."""
    def __init__(self, session, json_data=None, json_text=None):
        if json_text and not json_data:
            json_data = json.loads(json_text)
        elif json_data and not json_text:
            pass
        else:
            raise ValueError("Please provide either json_data, or json_text.")
        if not session:
            raise ValueError("session should be provided")
        self._session = session
        self._link_first = json_data["_links"]["first"]["href"]
        (self._link_next, self._items) = Collection.parse_page(json_data)

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
                (self._link_next, new_items) = Collection.parse_page(json_data)
                self._items += new_items

    def __iter__(self):
        return CollectionIterator(self)

    def get_iterator(self):
        return CollectionIterator(self)

    def get_generator(self):
        """Iterate over the result pages, in an efficient manner.
        Doesn't store previous pages. Just yield elements one after another,
        while fetching next elements when required."""
        return CollectionGenerator(self._session, self._items, self._link_first, self._link_next)

    @staticmethod
    def parse_page(json_data):
        """Returns (next link, retrieved items)"""
        final_next_link = None
        next_link = json_data["_links"].get('next')
        if next_link:
            final_next_link = next_link['href']
        # TODO : parse count as well (in php, $count = isset($data['items_count']) ? $data['items_count'] : null;)
        return (final_next_link, json_data["_embedded"]["items"])


class CollectionGenerator(object):
    def __init__(self, session, current_items, link_self, next_link):
        self._items = current_items
        self._link_next = next_link
        self._link_self = link_self
        self._session = session

    def __iter__(self):
        while True:
            for item in self._items:
                yield item
            if self._link_next:
                r = self._session.get(self._link_next)
                if r.status_code == 200:
                    self._link_self = self._link_next
                    (self._link_next, self._items) = Collection.parse_page(json.loads(r.text))
            else:
                break

    def get_next_link(self):
        return self._link_next

    def get_self_link(self):
        return self._link_self


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
