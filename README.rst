|Build Status|
|Documentation Status|


Python client for Akeneo PIM API
================================

A simple Python client to use the `Akeneo PIM API`_.

Dependencies are managed with `pipenv`_
(list of dependencies available in `Pipfile`_).

.. _Pipfile: Pipfile

You may install them with:

.. code:: bash

        pipenv install --dev

Installation
------------
The easiest is to use pipenv in your new project:

.. code:: bash

        pipenv install git+https://github.com/matthieudelaro/akeneo_api_client#egg=akeneo_api_client
        
Usage
-----

A simple example is provided in `docs/example.py`_.

.. _docs/example.py: https://raw.githubusercontent.com/matthieudelaro/akeneo_api_client/master/docs/example.py

To export the data from your PIM, you may use the `docs/example_exporter.py`_.

If you experience issues when importing modules, run the examples as follow:

.. code:: bash

        cd docs
        pipenv run python3 example_exporter.py
        

.. _docs/example_exporter.py: https://raw.githubusercontent.com/matthieudelaro/akeneo_api_client/master/docs/example_exporter.py

Tests
-----

Run tests as follow:

.. code:: bash

        pipenv run nosetests
        
If tests don't pass in your environment, please check that dependencies match those described in Pipfile. One way to do it is to ensure that pipenv runs commands in a dedicated virtualenv by setting environment variable as follow:

.. code:: bash

        export PIPENV_IGNORE_VIRTUALENVS=1
        pipenv install --dev  # (re)run installation of dependencies

Or even emulate Travis in Docker:

.. code:: bash

        # This will: 
        # - copy the current directory into a temporary directory, which will be mounted in (and modified by) a docker container
        # - run the container of Travis as explained here: https://stackoverflow.com/a/49019950
        # - run the steps of Travis thanks to wwtd: https://github.com/grosser/wwtd
        rm -rf /tmp/localTravis; cp -R . /tmp/localTravis; INSTANCE="travisci/ci-garnet:packer-1512502276-986baf0"; BUILDID="build-$RANDOM"; docker run --name $BUILDID -dit -v /tmp/localTravis:/home/travis/matthieudelaro/akeneo_api_client $INSTANCE /sbin/init; docker exec -it --user travis $BUILDID bash -lc "whoami; cd /home/travis/matthieudelaro/akeneo_api_client; gem install wwtd; source ~/virtualenv/python3.6/bin/activate; wwtd -u before_install -u install -u before_script -u language -u python; history; bash"


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
