from collections import namedtuple
import json


def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    https://stackoverflow.com/a/11326230
    """
    return "/".join(map(lambda x: str(x).strip('/').rstrip('/'), args))


def _json_object_hook(data):
    '''https://stackoverflow.com/a/15882054'''
    try:
        data['links'] = data.pop('_links')
    except KeyError as e:
        pass
    try:
        data['embedded'] = data.pop('_embedded')
    except KeyError as e:
        pass
    return namedtuple('X', data.keys(), rename=False)(*data.values())


def json2object(data):
    '''https://stackoverflow.com/a/15882054'''
    return json.loads(data, object_hook=_json_object_hook)