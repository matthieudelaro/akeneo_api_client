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