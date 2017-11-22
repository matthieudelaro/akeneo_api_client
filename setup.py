#!/usr/bin/env python
import os
import re
import sys

from codecs import open

from setuptools import setup
from setuptools.command.test import test as TestCommand
import subprocess

here = os.path.abspath(os.path.dirname(__file__))

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

packages = ['akeneo_api_client']

# requires = subprocess.run(["pipenv", "lock", "-r"],
#                               stdout=subprocess.PIPE).stdout.decode('utf-8')
requires = [
    'requests',
    'logzero', 'dotenv',
]
test_requirements = [
    'nose',
    'ipython',
    'vcrpy-unittest',
    'sphinx',
]

about = {}
with open(os.path.join(here, 'akeneo_api_client', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE'], 'requests': ['*.pem']},
    package_dir={'requests': 'requests'},
    include_package_data=True,
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    classifiers=(
        'Programming Language :: Python :: 3',
    ),
    tests_require=test_requirements,
)
