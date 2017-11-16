# -*- coding: utf-8 -*-

import json


class Result(object):
    """Holds the result of a search. It can be iterated through as a list,
    as an iterator, or as a generator. Note that only one iteration should be
    used on a given Collection object.
    Search results are paginated: https://api.akeneo.com/documentation/pagination.html

    The next page will be loaded once the user
    iterated over the whole current page. The content of the new page will replace
    the content of the previous page."""
    def __init__(self, session, count, current_items, link_first, link_next, link_self):
        self._items = current_items
        self._link_next = link_next
        self._link_self = link_self
        self._link_first = link_first
        self._count = count
        self._session = session
        self._page_iterator = iter(self._items)
        self._reached_the_end = False

    def __iter__(self):
        while not self._reached_the_end:
            for item in self._page_iterator:
                yield item
            self.fetch_next_page()

    def __next__(self):
        try:
            return next(self._page_iterator)
        except Exception:
            self.fetch_next_page()
            if not self._reached_the_end:
                return next(self._page_iterator)
            else:
                return

    def get_page_items(self):
        return self._items

    def fetch_next_page(self):
        """Return True if a next page exists. Returns False otherwise."""
        if self._link_next:
            r = self._session.get(self._link_next)
            if r.status_code == 200:
                (self._link_first, self._link_self, self._link_next, self._items, self._count) = Result.parse_page(json.loads(r.text))
                self._page_iterator = iter(self._items)
                self._reached_the_end = False
            else:
                self._reached_the_end = True
        else:
            self._reached_the_end = True
        return not self._reached_the_end

    def get_count(self):
        return self._count

    def get_next_link(self):
        return self._link_next

    def get_self_link(self):
        return self._link_self

    def get_first_link(self):
        return self._link_first

    @staticmethod
    def parse_page(json_data):
        """Returns (next link, retrieved items, count of items)"""
        final_next_link = None
        next_link = json_data["_links"].get('next')
        if next_link:
            final_next_link = next_link['href']
        return (
            json_data["_links"]["first"]["href"],
            json_data["_links"]["self"]["href"],
            final_next_link,
            json_data["_embedded"]["items"],
            json_data.get("items_count"),
        )

    @staticmethod
    def from_json_text(session, json_text):
        json_data = json.loads(json_text)
        parsed = Result.parse_page(json_data)
        return Result(session, parsed[4], parsed[3], parsed[0], parsed[2], parsed[1])
