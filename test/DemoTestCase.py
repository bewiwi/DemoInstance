import unittest
import requests
import json


class DemoTestCase(unittest.TestCase):
    config = {}

    def __init__(self, methodName='runTest'):
        super(DemoTestCase, self).__init__(methodName)

    def get(self, uri, params=None):
        r = requests.get(DemoTestCase.config["demo_url"]+uri, params=params)
        return r

    def put(self, uri, params=None):
        r = requests.put(DemoTestCase.config["demo_url"]+uri, params=params)
        return r

    def delete(self, uri, params=None):
        r = requests.delete(DemoTestCase.config["demo_url"]+uri, params=params)
        return r

    def post(self, uri, params=None):
        params = json.dumps(params)
        r = requests.post(DemoTestCase.config["demo_url"]+uri, data=params)
        return r
