# coding=utf-8
from auth import DemoAuth


class AuthFake(DemoAuth):
    def __init__(self, config):
        self.config = config

    def check_auth(self, user, password):
        if user in self.config:
            if password == self.config[user]:
                return user + '@fake.com'
        return False
