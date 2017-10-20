import requests
from requests.auth import AuthBase
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
import unittest
import base64
import json
from time import time

import logging
import logzero
from logzero import logger

class AkeneoAuth(AuthBase):
    TOKEN_PATH = "api/oauth/v1/token"
    TOKEN_EXPIRY_SECURITY = 60 * 2

    def __init__(self, base_url, client_id, secret, username, password):
        """
        :param base_url: eg http://localhost:8088/
        """
        self._base_url = base_url
        self._client_id = client_id
        self._secret = secret
        self._username = username
        self._password = password
        self._token = None
        self._refresh_token = None
        self._expiry_date = None

    @property
    def authorization(self):
        return 'Bearer {0}'.format(self._token)

    def _request_a_token(self, grant_type="password"):
        """Requests a token. Throws in case of error"""
        authorization = "Basic {0}".format(base64.b64encode(
            "{0}:{1}".format(self._client_id, self._secret).encode('ascii')
        ).decode('utf-8'))
        headers = {
            'Content-Type': 'application/json',
            'Authorization': authorization
        }
        if grant_type == 'password':
            data = json.dumps({
                'grant_type': "password",
                'username': self._username,
                'password': self._password
            })
        elif grant_type == 'refresh_token':
            data = json.dumps({
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token
            })
        else:
            raise ValueError('grant_type parameter is expected to be either ' +
                '"password" or "refresh_token". {0} provided'.format(grant_type))
        logger.debug(data)
        url = urljoin(self._base_url, self.TOKEN_PATH)
        r = requests.post(url, data=data, headers=headers)
        if r.status_code != 200:
            raise requests.HTTPError("Status code: {0}".format(r.status_code))

        try:
            json_data = json.loads(r.text)
        except json.decoder.JSONDecodeError as e:
            raise SyntaxError("The server did not return expected json: {0}"
                .format(r.text))
        logger.debug(r.status_code)
        logger.debug(r.encoding)
        logger.debug(json.dumps(json_data, indent=4, sort_keys=True))
        try:
            self._token = json_data['access_token']
            self._refresh_token = json_data['refresh_token']
        except KeyError as e:
            raise SyntaxError("The server did not return expected tokens: {0}"
                .format(json_data))

        try:
            self._expiry_date = time() + float(json_data['expires_in'])
        except KeyError as e:
            self._expiry_date = None
        except ValueError as e:
            raise SyntaxError("The server did not return a valid expires_in: {0}"
                .format(json_data))
        logger.debug(self.authorization)
        logger.debug(self._refresh_token)
        logger.debug(self._expiry_date)


    def _should_refresh_token(self):
        """Returns True if the token is expired / about to expire"""
        if not self._expiry_date:
            return True
        else:
            return time() > self._expiry_date - self.TOKEN_EXPIRY_SECURITY


    def _refresh_the_token(self):
        """Requests a new token based on refresh token."""
        return self._request_a_token(grant_type='refresh_token')


    def __call__(self, r):
        
        if not self._token:
            self._request_a_token()
        if self._should_refresh_token():
            self._refresh_the_token()
        
        r.headers['Authorization'] = self.authorization
        # r.headers[] = 
        return r


class TestAuthIntegration(unittest.TestCase):
    client_id = 'xxx'
    secret = 'xxx'
    username = 'admin'
    password = 'admin'
    base_url = 'http://localhost:8080'

    def setUp(self):
        pass

    def test_valid(self):
        auth = AkeneoAuth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        auth._request_a_token()
        auth._refresh_the_token()

    def test_invalid_request(self):
        auth = AkeneoAuth(self.base_url,
            self.client_id, "fake secret", self.username, self.password)
        with self.assertRaises(requests.exceptions.HTTPError):
            auth._request_a_token()

    def test_invalid_refresh(self):
        auth = AkeneoAuth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        auth._request_a_token()
        with self.assertRaises(requests.exceptions.HTTPError):
            auth._refresh_token = "coucou"
            auth._refresh_the_token()

    def test_should_refresh_request(self):
        auth = AkeneoAuth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        auth._request_a_token()
        logger.debug(int(time()))
        logger.debug(auth._expiry_date)
        self.assertFalse(auth._should_refresh_token())
        auth._expiry_date = time() - 100
        self.assertTrue(auth._should_refresh_token())

    def test_query_products_with_auth(self):
        auth = AkeneoAuth(self.base_url,
            self.client_id, self.secret, self.username, self.password)
        r = requests.get(urljoin(self.base_url, "/api/rest/v1/products"), auth=auth)
        logger.debug(r)
        logger.debug(r.status_code)
        json_data = json.loads(r.text)
        logger.debug(json.dumps(json_data, indent=4, sort_keys=True))

# """
# {
#     "access_token": "ZGM1NTVjNzZlZWQ5Yzc0MWM5NGU1NDhjMzEyZjliZTcwYThlYjAxMTIxMmNiOTUxM2JkMTVlODM4YjZjMjNlNA",
#     "expires_in": 3600,
#     "refresh_token": "Y2E4YWRlNzgwNjY4ZDVkY2ZiOGRmOTc4YmQwZTE5ZGRmYjE5YWIyZDM3YzhiODUxZWI3MTljMWMzOGFiNDMwYw",
#     "scope": null,
#     "token_type": "bearer"
# }"""
        # self.assertEqual(, second)
        # res = self.c.parseFile("examples/validExample.txt")
        # self.assertEqual(res, "")

        # res = self.c.convert()

        # res = self.c.formatOutput(res)
        # self.assertEqual(res, "23.70")


if __name__ == '__main__':
    logzero.loglevel(logging.INFO)
    unittest.main()

