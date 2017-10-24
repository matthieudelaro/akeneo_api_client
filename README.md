# Python client for Akeneo PIM API

A simple Python client to use the [Akeneo PIM API](https://api.akeneo.com/).

Dependencies are managed with [pipenv](https://github.com/kennethreitz/pipenv).

## Usage
A simple example is provided in `./example.py`:
```python
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
```



## Tests
Run tests as follow:
```bash
    pipenv run nosetests
```

Tests are provided with mocks, recorded with [VCR.py](http://vcrpy.readthedocs.io/en/latest/index.html).
In case you need to (re)run tests, you should install the dataset in you PIM
instance as follow:
- specify the database to install in `app/config/parameters.yml`:
```yaml
    installer_data: PimInstallerBundle:icecat_demo_dev
```
- install the database by running the following command:
```bash
	bin/console pim:installer:db --env=prod
	# or, in case you are using Docker:
	docker-compose exec fpm bin/console pim:installer:db --env=prod
```