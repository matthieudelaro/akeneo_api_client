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
        self._link_first = json_data["_links"]["first"]
        (self._link_next, self._items) = self._parse_page(json_data)

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
                (self._link_next, new_items) = self._parse_page(json_data)
                self._items += new_items

    def _parse_page(self, json_data):
        final_next_link = None
        next_link = json_data["_links"].get('next')
        if next_link:
            final_next_link = next_link['href']
        # TODO : parse count as well (in php, $count = isset($data['items_count']) ? $data['items_count'] : null;)
        return (final_next_link, json_data["_embedded"]["items"])

    def __iter__(self):
        return CollectionIterator(self)

    def get_iterator(self):
        return CollectionIterator(self)

    def get_generator(self):
        """Iterate over the result pages, in an efficient manner.
        Doesn't store previous pages. Just yield elements one after another,
        while fetching next elements when required."""
        items = self._items
        link_next = self._link_next
        while True:
            for item in items:
                yield item
            if link_next:
                r = self._session.get(link_next)
                if r.status_code == 200:
                    (link_next, items) = self._parse_page(json.loads(r.text))
            else:
                break



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
