import requests
from requests.auth import AuthBase
from akeneo_api_client.utils import urljoin
import base64
import json
from time import time

from logzero import logger


class Auth(AuthBase):
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
        url = urljoin(self._base_url, self.TOKEN_PATH)
        r = requests.post(url, data=data, headers=headers)
        if r.status_code != 200:
            raise requests.HTTPError("Status code: {0}".format(r.status_code))

        try:
            json_data = json.loads(r.text)
        except json.decoder.JSONDecodeError as e:
            raise SyntaxError("The server did not return expected json: {0}"
                .format(r.text))
        try:
            self._token = json_data['access_token']
            self._refresh_token = json_data['refresh_token']
        except KeyError:
            raise SyntaxError("The server did not return expected tokens: {0}"
                              .format(json_data))

        try:
            self._expiry_date = time() + float(json_data['expires_in'])
        except KeyError:
            self._expiry_date = None
        except ValueError:
            raise SyntaxError("The server did not return a valid expires_in: {0}"
                .format(json_data))

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
        return r
