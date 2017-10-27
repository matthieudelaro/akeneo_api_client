|Build Status|
|Documentation Status|


Python client for Akeneo PIM API
================================

A simple Python client to use the `Akeneo PIM API`_.

Dependencies are managed with `pipenv`_.

Usage
-----

A simple example is provided in ``/example.py``:

.. literalinclude:: example.py

Tests
-----

Run tests as follow:

.. code:: bash

        pipenv run nosetests

Tests are provided with mocks, recorded with `VCR.py`_. In case you need
to (re)run tests, you should install the dataset in you PIM instance as
follow:

- specify the database to install in app/config/parameters.yml:

.. code:: yaml

        installer_data: PimInstallerBundle:icecat_demo_dev

-  install the database by running the following command:

   .. code:: bash

       bin/console pim:installer:db --env=prod
       # or, in case you are using Docker:
       docker-compose exec fpm bin/console pim:installer:db --env=prod

.. _Akeneo PIM API: https://api.akeneo.com/
.. _pipenv: https://github.com/kennethreitz/pipenv
.. _VCR.py: http://vcrpy.readthedocs.io/en/latest/index.html

.. |Build Status| image:: https://travis-ci.org/matthieudelaro/akeneo_api_client.svg?branch=master
   :target: https://travis-ci.org/matthieudelaro/akeneo_api_client
.. |Documentation Status| image:: https://readthedocs.org/projects/akeneo-api-client/badge/?version=latest
   :target: http://akeneo-api-client.readthedocs.io/en/latest/