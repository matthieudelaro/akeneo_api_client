# -*- coding: utf-8 -*-

import abc

class GettableResourceInterface(abc.ABC):
    @abc.abstractmethod
    def fetch_item(self, code):
        pass

class ListableResourceInterface(abc.ABC):
    @abc.abstractmethod
    def fetch_list(self, **kwargs):
        pass

class CreatableResourceInterface(abc.ABC):
    @abc.abstractmethod
    def create_item(self, item):
        pass

class DeletableResourceInterface(abc.ABC):
    @abc.abstractmethod
    def delete_item(self, code):
        pass

class CodeBasedResourceInterface(abc.ABC):
    @abc.abstractmethod
    def get_code(self, item):
        pass

