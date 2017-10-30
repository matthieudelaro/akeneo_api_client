# -*- coding: utf-8 -*-

# Reduce the amount of logs:
import logging
import logzero
from logzero import logger
logzero.loglevel(logging.WARN)

# fetch products from your PIM:
from akeneo_api_client.client import Client
import json

client_id = 'XXX'
secret = 'XXX'
username = 'admin'
password = 'admin'
base_url = 'http://localhost:8080'

akeneo = Client(base_url,
    client_id, secret, username, password)

# create and delete items, such as products:
valid_product = """{"identifier":"myawesometshirt","enabled":true,"family":"clothing","categories":["master_men_blazers"],"groups":[],"parent":null,"values":{"collection":[{"data":["summer_2017"],"locale":null,"scope":null}],"color":[{"data":"white","locale":null,"scope":null}],"description":[{"data":"Biker jacket","locale":"en_US","scope":"ecommerce"}],"ean":[{"data":"1234567946367","locale":null,"scope":null}],"material":[{"data":"polyester","locale":null,"scope":null}],"name":[{"data":"Biker jacket","locale":null,"scope":null}],"price":[{"data":[{"amount":null,"currency":"EUR"},{"amount":null,"currency":"USD"}],"locale":null,"scope":null}],"size":[{"data":"xl","locale":null,"scope":null}],"variation_name":[{"data":"Biker jacket polyester","locale":"en_US","scope":null}]}}"""
akeneo.products.create_item(json.loads(valid_product))
akeneo.products.delete_item('myawesometshirt')

# fetch items or list of items:
single_item = akeneo.products.fetch_item('1111111137')
items = akeneo.products.fetch_list()

# you may then use those items as a list:
print(items.get_list())
print(len(items.get_list())) # 10


# you may even iterate over it with an iterator,
# which will fetch next pages seamlessly as you iterate over it:
iterator = iter(items)
for i in range(200):
    item = next(iterator)
print(len(items.get_list())) # 200
# See Akeneo and Pagination: https://api.akeneo.com/documentation/pagination.html

# When using the iterator, all the items are kept in memory.
# This is an issue when processing a large amount of data.
# In this case, better use the generator:
lots_of_items = akeneo.products.fetch_list()
for item in lots_of_items.get_generator():
	print(item)
print(len(items.get_list())) # 10, ie the size of the page,
# instead of the total amount of items that have been fetched.



