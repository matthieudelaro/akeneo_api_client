# -*- coding: utf-8 -*-

# Reduce the amount of logs:
import logging
import logzero
from logzero import logger
logzero.loglevel(logging.WARN)

# fetch products from your PIM:
from akeneo_api_client.client import Client

client_id = 'XXXX'
secret = 'XXX'
username = 'admin'
password = 'admin'
base_url = 'http://localhost:8080'

akeneo = Client(base_url,
    client_id, secret, username, password)
single_item = akeneo.products.fetch_item('1111111137')
items = akeneo.products.fetch_list()

# you may use fetched items as a list:
print(items.get_list())

# or iterate over it with an iterator:
iterator = iter(items)
for i in range(200):
    item = next(iterator)
    # the iterator will fetch the next page of elements as you iterate through
    # the list, seamlessly 
