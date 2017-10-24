# -*- coding: utf-8 -*-

import abc

class GettableResourceInterface(abc.ABC):
    @abc.abstractmethod
    def fetch_item(self, identifier):
        pass

class ListableResourceInterface(abc.ABC):
    @abc.abstractmethod
    def fetch_list(self, **kwargs):
        pass

class CreatableResourceInterface(abc.ABC):
    @abc.abstractmethod
    def create_item(self, item):
        pass
