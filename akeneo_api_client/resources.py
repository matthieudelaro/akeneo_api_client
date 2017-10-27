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
    def fetch_list(self, args=None):
        """Send a request with search, etc.
        Returns an iterable list (Collection)"""
        if args:
            for (key,value) in args.items():
                if not isinstance(value, str):
                    args[key] = json.dumps(value)

        url = self._endpoint
        r = self._session.get(url, params=args)

        if r.status_code != 200:
            raise requests.HTTPError("Status code: {0}. Content: {1}".format(
                r.status_code,
                r.text))

        c = Collection(self._session, json_text=r.text)
        return c


class SearchAfterListableResource(ListableResource):
    def fetch_list(self, args=None):
        """Send a request with search, etc.
        Returns an iterable list (Collection)"""
        params = args
        if not params:
            params = {"pagination_type": "search_after"}
        elif "pagination_type" not in params:
            params['pagination_type'] = 'search_after'

        return super(SearchAfterListableResource, self).fetch_list(params)


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


class UpdatableResource(UpdatableResourceInterface):
    def update_create_item(self, item_values, code=None):
        if not code:
            code = self.get_code(item_values)

        url = urljoin(self._endpoint, code)
        logger.debug(json.dumps(item_values, separators=(',', ':')))
        r = self._session.patch(url, data=json.dumps(item_values, separators=(',', ':')))

        if r.status_code not in [201, 204]:
            raise requests.HTTPError("Status code: {0}. Content: {1}".format(
                r.status_code,
                r.text))
        else:
            return r.headers.get('Location')


class UpdatableListResource(UpdatableResourceInterface):
    def update_create_list(self, item_values, code=None):
        raise NotImplementedError()

class IdentifierBasedResource(CodeBasedResourceInterface):
    def get_code(self, item):
        return item['identifier']

class CodeBasedResource(CodeBasedResourceInterface):
    def get_code(self, item):
        return item['code']

class ResourcePool():
    def __init__(self, endpoint, session):
        """Initialize the ResourcePool to the given endpoint. Eg: products"""
        self._endpoint = endpoint
        self._session = session
        pass

class ProductsPool(ResourcePool,
        IdentifierBasedResource,
        CreatableResource,
        DeletableResource,
        GettableResource,
        SearchAfterListableResource,
        UpdatableResource,
        UpdatableListResource):
    """https://api.akeneo.com/api-reference.html#Products"""
    # TODO: EE support of drafts
    pass

class ProductModelsPool(ResourcePool,
        IdentifierBasedResource,
        CreatableResource,
        GettableResource,
        SearchAfterListableResource,
        UpdatableResource,):
    """https://api.akeneo.com/api-reference.html#Productmodels"""
    pass

class PublishedProductsPool(ResourcePool,
        IdentifierBasedResource,
        GettableResource,
        SearchAfterListableResource,):
    """https://api.akeneo.com/api-reference.html#Publishedproducts"""
    pass

class CategoriesPool(ResourcePool,
    CodeBasedResource,
    CreatableResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
    UpdatableListResource,):
    """https://api.akeneo.com/api-reference.html#Categories"""
    pass

class FamilyVariantsPool(ResourcePool,
    CodeBasedResource,
    CreatableResource,
    GettableResource,
    ListableResource,):
    """https://api.akeneo.com/api-reference.html#Families"""
    pass

class FamiliesPool(ResourcePool,
    CodeBasedResource,
    CreatableResource,
    DeletableResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
    UpdatableListResource,):
    """https://api.akeneo.com/api-reference.html#Families"""
    def variants(self, code):
        return FamilyVariantsPool(
            urljoin(self._endpoint, code, 'variants/'),
            self._session
        )

class AttributeOptionsPool(ResourcePool,
    CodeBasedResource,
    CreatableResource,
    GettableResource,
    ListableResource,
    UpdatableResource,):
    """https://api.akeneo.com/api-reference.html#Attributeoptions"""
    pass

class AttributesPool(ResourcePool,
    CodeBasedResource,
    CreatableResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
    UpdatableListResource,):
    """https://api.akeneo.com/api-reference.html#Attributes"""
    def options(self, code):
        return AttributeOptionsPool(
            urljoin(self._endpoint, code, 'options/'),
            self._session
        )

class AttributeGroupsPool(ResourcePool,
    CodeBasedResource,
    ListableResource,
    CreatableResource,
    UpdatableListResource,
    GettableResource,
    UpdatableResource,):
    """https://api.akeneo.com/api-reference.html#Attributegroups"""
    pass

class MediaFilesPool(ResourcePool,
    CodeBasedResource,
    ListableResource,
    CreatableResource,
    GettableResource,):
    """https://api.akeneo.com/api-reference.html#Mediafiles"""
    def download(self, code):
        raise NotImplementedError()
    pass

class LocalesPool(ResourcePool,
    CodeBasedResource,
    ListableResource,
    GettableResource,):
    """https://api.akeneo.com/api-reference.html#Locales"""
    pass

class ChannelsPool(ResourcePool,
    CodeBasedResource,
    ListableResource,
    UpdatableListResource,
    GettableResource,
    UpdatableResource,):
    """https://api.akeneo.com/api-reference.html#Channels"""
    pass

class CurrenciesPool(ResourcePool,
    CodeBasedResource,
    ListableResource,
    CreatableResource,):
    """https://api.akeneo.com/api-reference.html#Currencies"""
    pass

class MeasureFamiliesPool(ResourcePool,
    CodeBasedResource,
    ListableResource,
    GettableResource,):
    """https://api.akeneo.com/api-reference.html#Measurefamilies"""
    pass

class AssociationTypesPool(ResourcePool,
    CodeBasedResource,
    ListableResource,
    CreatableResource,
    UpdatableListResource,
    GettableResource,
    UpdatableResource,):
    """https://api.akeneo.com/api-reference.html#Associationtypes"""
    pass
