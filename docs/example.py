# -*- coding: utf-8 -*-

# Reduce the amount of logs:
import json
import os
import logging
import logzero

logzero.loglevel(logging.WARN)

# import Akeneo API Client
try:
    from akeneo_api_client.client import Client
except ModuleNotFoundError as e:
    import sys
    sys.path.append("..")
    from akeneo_api_client.client import Client

# Import your API keys from environment variables
# which may be inflated from a .env file for example
# See https://github.com/theskumar/python-dotenv
try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
except ModuleNotFoundError as e:
    print("dotenv is unavailable. So make sure you provided "
          "AKENEO_CLIENT_ID, AKENEO_SECRET, AKENEO_USERNAME, "
          "AKENEO_PASSWORD, and AKENEO_BASE_URL "
          "as environment variables.")
logzero.loglevel(logging.INFO)

AKENEO_CLIENT_ID = os.environ.get("AKENEO_CLIENT_ID")
AKENEO_SECRET = os.environ.get("AKENEO_SECRET")
AKENEO_USERNAME = os.environ.get("AKENEO_USERNAME")
AKENEO_PASSWORD = os.environ.get("AKENEO_PASSWORD")
AKENEO_BASE_URL = os.environ.get("AKENEO_BASE_URL")

akeneo = Client(AKENEO_BASE_URL, AKENEO_CLIENT_ID,
                AKENEO_SECRET, AKENEO_USERNAME, AKENEO_PASSWORD)

# fetch items or list of items:
try:
    single_item = akeneo.products.fetch_item('1111111137')
except Exception as e:
    print('1111111137 is not likely to exist in your PIM. Indeed:')
    print(e)
result = akeneo.products.fetch_list()

# you may then use those items as a list:
print(result.get_page_items())  # print the items of the first page
print(len(result.get_page_items()))  # 10

# you may even iterate over it with an iterator,
# which will fetch next pages seamlessly as you iterate over it:
for item in result:
    print(item["identifier"])  # this will fetch all products from the PIM, and display their identifiers
# if you want to fetch only the first 50 products:
for i in range(50):
    item = next(result)
    print(item["identifier"])


# See Akeneo and Pagination: https://api.akeneo.com/documentation/pagination.html


# create and delete items, such as products:
def modify_content():
    valid_product = """{"identifier":"myawesometshirt","enabled":true,"family":"clothing","categories":[
    "master_men_blazers"],"groups":[],"parent":null,"values":{"collection":[{"data":["summer_2017"],"locale":null,
    "scope":null}],"color":[{"data":"white","locale":null,"scope":null}],"description":[{"data":"Biker jacket",
    "locale":"en_US","scope":"ecommerce"}],"ean":[{"data":"1234567946367","locale":null,"scope":null}],"material":[{
    "data":"polyester","locale":null,"scope":null}],"name":[{"data":"Biker jacket","locale":null,"scope":null}],
    "price":[{"data":[{"amount":null,"currency":"EUR"},{"amount":null,"currency":"USD"}],"locale":null,
    "scope":null}],"size":[{"data":"xl","locale":null,"scope":null}],"variation_name":[{"data":"Biker jacket 
    polyester","locale":"en_US","scope":null}]}} """
    akeneo.products.create_item(json.loads(valid_product))
    akeneo.products.delete_item('myawesometshirt')
