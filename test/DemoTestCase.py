import unittest
import requests
import json


class DemoTestCase(unittest.TestCase):
    config = {}

    def __init__(self, methodName='runTest'):
        super(DemoTestCase, self).__init__(methodName)
        self.cookies = {}

    def get(self, uri, params=None):
        params = json.dumps(params)
        r = requests.get(
            DemoTestCase.config["demo_url"]+uri,
            data=params,
            cookies=self.cookies
        )
        return r

    def put(self, uri, params=None):
        params = json.dumps(params)
        r = requests.put(
            DemoTestCase.config["demo_url"]+uri,
            data=params,
            cookies=self.cookies
        )
        return r

    def delete(self, uri, params=None):
        params = json.dumps(params)
        r = requests.delete(
            DemoTestCase.config["demo_url"]+uri,
            data=params,
            cookies=self.cookies
        )
        return r

    def post(self, uri, params=None):
        params = json.dumps(params)
        r = requests.post(
            DemoTestCase.config["demo_url"]+uri,
            data=params,
            cookies=self.cookies
        )
        return r

    def login(self, user, password):
        r = self.post(
            '/api/connect',
            {'user': user, 'password': password}
        )
        self.cookies['token'] = r.cookies['token']

    def logout(self):
        self.cookies['token'] = False

    def rep_to_dict(self, text):
        return json.loads(text)
