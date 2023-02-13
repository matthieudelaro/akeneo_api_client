# -*- coding: utf-8 -*-

from akeneo_api_client.utils import *
from akeneo_api_client.interfaces import *
from akeneo_api_client.result import *
import requests
import json

from logzero import logger

import math


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
            for (key, value) in args.items():
                if not isinstance(value, str):
                    args[key] = json.dumps(value)

        url = self._endpoint
        r = self._session.get(url, params=args)

        if r.status_code != 200:
            raise requests.HTTPError("Status code: {0}. Content: {1}".format(
                r.status_code,
                r.text))

        # c = Collection(self._session, json_text=r.text)
        c = Result.from_json_text(self._session, json_text=r.text)
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
    def fetch_item(self, code_or_item):
        """Returns a unique item object. code_or_item should be a the code
        of the desired item, or an item with the proper code."""
        code = code_or_item
        if not isinstance(code_or_item, str):
            # if code_or_item is item, then fetch the code
            code = self.get_code(code_or_item)

        logger.debug(self._endpoint)
        url = urljoin(self._endpoint, code)
        logger.debug(url)
        r = self._session.get(url)

        if r.status_code != 200:
            raise requests.HTTPError("The item {0} doesn't exit: {1}".format(code, r.status_code))

        logger.debug(r.status_code)
        logger.debug(r.text)
        return json.loads(r.text)  # returns item as a dict


class DeletableResource(DeletableResourceInterface):
    def delete_item(self, code_or_item):
        """code_or_item should be a the code
        of the desired item, or an item with the proper code."""
        code = code_or_item
        if not isinstance(code_or_item, str):
            # if code_or_item is item, then fetch the code
            code = self.get_code(code_or_item)
        url = urljoin(self._endpoint, code)
        r = self._session.delete(url)

        if r.status_code != 204:
            raise requests.HTTPError("The item {0} doesn't exit. Content: {1}".format(
                code,
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
    def update_create_list(self, items, code=None):
        url = self._endpoint
        data = ""
        for item in items:
            data += json.dumps(item, separators=(',', ':')) + '\n'
        r = self._session.patch(url, data=data, headers={'Content-type': 'application/vnd.akeneo.collection+json'})

        if r.status_code == 413:
            # TODO handle 413
            # Request Entity Too Large
            # There are too many resources to process (max 100)
            # =>>>>> or the line of JSON is too long (max 1 000 000 characters)
            # split the list in several chunks
            num = 100
            n = math.ceil(len(items) / num)

            itemss = [items[i:i + num] for i in range(0, (n - 1) * num, num)]
            itemss.append(items[(n - 1) * num:])

            return [item
                    for those_items in itemss
                    for item in self.update_create_list(those_items)]

        if r.status_code != 200:
            raise requests.HTTPError("Status code: {0}. Content: {1}".format(
                r.status_code,
                r.text))

        else:
            statuses = []
            for line in r.text.split('\n'):
                statuses.append(json.loads(line))
            return statuses


class IdentifierBasedResource(CodeBasedResourceInterface):
    def get_code(self, item):
        return item['identifier']


class CodeBasedResource(CodeBasedResourceInterface):
    def get_code(self, item):
        return item['code']


class EnterpriseEditionResource():
    pass


class ResourcePool():
    def __init__(self, endpoint, session):
        """Initialize the ResourcePool to the given endpoint. Eg: products"""
        self._endpoint = endpoint
        self._session = session
        pass

    def get_url(self):
        return self._endpoint


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
                        UpdatableResource, ):
    """https://api.akeneo.com/api-reference.html#Productmodels"""
    pass


class PublishedProductsPool(ResourcePool,
                            IdentifierBasedResource,
                            GettableResource,
                            SearchAfterListableResource,
                            EnterpriseEditionResource, ):
    """https://api.akeneo.com/api-reference.html#Publishedproducts"""
    pass


class CategoriesPool(ResourcePool,
                     CodeBasedResource,
                     CreatableResource,
                     GettableResource,
                     ListableResource,
                     UpdatableResource,
                     UpdatableListResource, ):
    """https://api.akeneo.com/api-reference.html#Categories"""
    pass


class FamilyVariantsPool(ResourcePool,
                         CodeBasedResource,
                         CreatableResource,
                         GettableResource,
                         ListableResource, ):
    """https://api.akeneo.com/api-reference.html#Families"""
    pass


class FamiliesPool(ResourcePool,
                   CodeBasedResource,
                   CreatableResource,
                   DeletableResource,
                   GettableResource,
                   ListableResource,
                   UpdatableResource,
                   UpdatableListResource, ):
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
                           UpdatableResource, ):
    """https://api.akeneo.com/api-reference.html#Attributeoptions"""
    pass


class AttributesPool(ResourcePool,
                     CodeBasedResource,
                     CreatableResource,
                     GettableResource,
                     ListableResource,
                     UpdatableResource,
                     UpdatableListResource, ):
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
                          UpdatableResource, ):
    """https://api.akeneo.com/api-reference.html#Attributegroups"""
    pass


class MediaFilesPool(ResourcePool,
                     CodeBasedResource,
                     ListableResource,
                     CreatableResource,
                     GettableResource, ):
    """https://api.akeneo.com/api-reference.html#Mediafiles"""

    def download(self, code):
        # TODO: implement this method
        raise NotImplementedError()

    pass


class LocalesPool(ResourcePool,
                  CodeBasedResource,
                  ListableResource,
                  GettableResource, ):
    """https://api.akeneo.com/api-reference.html#Locales"""
    pass


class ChannelsPool(ResourcePool,
                   CodeBasedResource,
                   ListableResource,
                   UpdatableListResource,
                   GettableResource,
                   UpdatableResource, ):
    """https://api.akeneo.com/api-reference.html#Channels"""
    pass


class CurrenciesPool(ResourcePool,
                     CodeBasedResource,
                     ListableResource,
                     CreatableResource, ):
    """https://api.akeneo.com/api-reference.html#Currencies"""
    pass


class MeasureFamiliesPool(ResourcePool,
                          CodeBasedResource,
                          ListableResource,
                          GettableResource, ):
    """https://api.akeneo.com/api-reference.html#Measurefamilies"""
    pass


class AssociationTypesPool(ResourcePool,
                           CodeBasedResource,
                           ListableResource,
                           CreatableResource,
                           UpdatableListResource,
                           GettableResource,
                           UpdatableResource, ):
    """https://api.akeneo.com/api-reference.html#Associationtypes"""
    pass


class AssetsPool(ResourcePool,
                 CodeBasedResource,
                 GettableResource,
                 ListableResource,
                 UpdatableResource,
                 UpdatableListResource,
                 DeletableResource,):
    pass


class AssetFamilyPool(ResourcePool,
                      CodeBasedResource,
                      GettableResource,
                      ListableResource,
                      UpdatableResource,):

    def assets(self, code):
        return AssetsPool(
            urljoin(self._endpoint, code, 'assets/'),
            self._session
        )


class ReferenceEntityRecordPool(
    ResourcePool,
    CodeBasedResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
    UpdatableListResource,
):
    pass


class ReferenceEntityPool(
    ResourcePool,
    CodeBasedResource,
    GettableResource,
    ListableResource,
    UpdatableResource,
):
    def records(self, entity_code):
        return ReferenceEntityRecordPool(
            urljoin(self._endpoint, entity_code, "records/"), self._session
        )
