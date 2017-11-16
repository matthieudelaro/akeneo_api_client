# -*- coding: utf-8 -*-
"""Will extract data from the PIM and pickle it to files."""

# Reduce the amount of logs:
import logging
import logzero
from logzero import logger

import sys
import pickle
import os

# Import your API keys from environment variables
# which may be inflated from a .env file for example
# See https://github.com/theskumar/python-dotenv
from dotenv import load_dotenv, find_dotenv

sys.path.append("..")
from akeneo_api_client.client import Client

load_dotenv(find_dotenv())
logzero.loglevel(logging.INFO)

AKENEO_CLIENT_ID = os.environ.get("AKENEO_CLIENT_ID")
AKENEO_SECRET = os.environ.get("AKENEO_SECRET")
AKENEO_USERNAME = os.environ.get("AKENEO_USERNAME")
AKENEO_PASSWORD = os.environ.get("AKENEO_PASSWORD")
AKENEO_BASE_URL = os.environ.get("AKENEO_BASE_URL")


class Extractor(object):
    @staticmethod
    def extract_all_resources(client, directory, request_limit=100, chunk_size=10000):
        for name, pool in client.resources.items():
            Extractor.extract_resource(pool, os.path.join(directory, name),
                                       request_limit=request_limit, chunk_size=chunk_size)

    @staticmethod
    def extract_resource(pool, directory, request_limit=100, chunk_size=10000):
        """Extract all items offered by the given endpoint. Saves them in
        files in the given directory, in buckets."""

        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            result = pool.fetch_list({'limit': request_limit})
        except Exception as e:
            logger.warning('''Skipping {name} :
                Does the version of the server support this endpoint?
                {error}'''.format(name=pool.get_url(), error=e))
        else:
            def save(directory, count, chunk, link):
                """Save a chunk to a file, as well as the next link of the last page."""
                if link:  # save the link, if there is a next page
                    link_filename = os.path.join(directory, '{0:07d}_next_link.txt'.format(count))
                    with open(link_filename, "w") as of:
                        of.write(link)

                chunk_filename = os.path.join(directory, '{0:07d}_chunk.p'.format(count))
                logger.info("Saving to {0}".format(chunk_filename))
                with open(chunk_filename, "wb") as of:
                    pickle.dump(chunk, of)

                return chunk_filename

            try:
                count = 0
                chunk = []
                chunk_filenames = []  # name of chunks saved to files
                logger.info('Fetching from {0}'.format(pool.get_url()))

                go_on = True
                while go_on:
                    chunk += result.get_page_items()
                    count += len(result.get_page_items())
                    go_on = result.fetch_next_page()
                    if (chunk and not go_on) or (len(chunk) >= chunk_size):
                        chunk_filenames.append(save(
                            directory, count, chunk, result.get_next_link()
                        ))
                        chunk = []
            except Exception as e:
                logger.error('Error while fetching {name}...:\n{next_link}\n{error}\n'.format(
                    name=pool.get_url(), next_link=result.get_next_link(), error=e))
                raise e


if __name__ == '__main__':
    client = Client(AKENEO_BASE_URL, AKENEO_CLIENT_ID,
                    AKENEO_SECRET, AKENEO_USERNAME, AKENEO_PASSWORD)
    Extractor.extract_all_resources(client, 'extract')
